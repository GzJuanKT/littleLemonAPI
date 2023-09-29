from requests import RequestException
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import permissions
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from . import models
from . import serializers
from .forms import UserRegistrationForm, UserLoginForm
# Create your views here.


def index(request):
    return render(request, 'base.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logintemplate_api')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@api_view(['POST'])
def login_user(request):
    print(request.data)
    username = request.data.get('username', None)
    if username is None:
        return Response({'message': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, username=username)

    if not user.check_password(request.data['password']):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            # Autenticar al usuario
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # Iniciar sesión si la autenticación es exitosa
                login(request, user)
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed!")


def all_users(request):
    return render(request, 'allUsers.html')


class menuItemsPagination(PageNumberPagination):
    page_size = 5  # Num de elementos por página
    page_size_query_param = 'page_size'
    # Size max de la página, 10 paginas * 5 items per page = 50 items en la db
    max_page_size = 10


class menuItems(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'price']
    ordering_fields = ['title', 'price']
    pagination_class = menuItemsPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST' and self.request.user.groups.filter(name='Manager').exists():
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        # Esta función se llama cuando se crea un nuevo objeto
        if self.request.user.groups.filter(name='Manager').exists():
            serializer.save()  # Solo los usuarios en el grupo Manager pueden crear

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'Only Managers are allowed to create.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticatedOrReadOnly])
def menuSingleItem(request, pk):
    items = get_object_or_404(models.MenuItem, pk=pk)

    if request.method == 'GET':
        serialized_items = serializers.MenuItemSerializer(items)
        return Response(serialized_items.data)

    if request.method in ['PUT', 'PATCH']:
        if request.user.groups.filter(name='Manager').exists():
            serialized_items = serializers.MenuItemSerializer(items,
                                                              data=request.data,
                                                              partial=request.method == 'PATCH')

            if serialized_items.is_valid():
                serialized_items.save()
                return Response(serialized_items.data, status=status.HTTP_200_OK)
            return Response(serialized_items.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'You have to be a manager to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You have to be a manager to perform this action'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAdminUser])
def listAddUsersManagerGroup(request):
    manager_group = Group.objects.get(name='Manager')

    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            managers = manager_group.user_set.all()
            serialized_managers = serializers.UserSerializer(
                managers, many=True)
            return Response(serialized_managers.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You have to be a manager to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            if manager_group.user_set.filter(username=username).exists():
                return Response({'message': 'User already exists in the Manager group'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = get_object_or_404(User, username=username)
                except User.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                if not user.is_staff:
                    user.is_staff = True
                    user.save()

                manager_group.user_set.add(user)
                return Response({'message': 'User added to the Manager group successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def removeUserManagerGroup(request, id):
    manager_group = Group.objects.get(name='Manager')
    user = get_object_or_404(User, id=id)

    if request.method == 'DELETE':
        if manager_group.user_set.filter(id=id).exists():
            if user.is_staff:
                user.is_staff = False
                user.save()
            manager_group.user_set.remove(user)
            return Response({'message': 'User removed from the Manager group successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found in the Manager group'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAdminUser])
def listAddUsersDeliveryCrewGroup(request):
    delivery_group = Group.objects.get(name='DeliveryCrew')

    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            deliveryUser = delivery_group.user_set.all()
            serialized_managers = serializers.UserSerializer(
                deliveryUser, many=True)
            return Response(serialized_managers.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You have to be a manager to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            if delivery_group.user_set.filter(username=username).exists():
                return Response({'message': 'User already exists in the DeliveryCrew group'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = get_object_or_404(User, username=username)
                except User.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                delivery_group.user_set.add(user)
                return Response({'message': 'User added to the DeliveryCrew group successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAdminUser])
def removeUserDeliveryCrewGroup(request, id):
    delivery_group = Group.objects.get(name='DeliveryCrew')
    user = get_object_or_404(User, id=id)

    if request.method == 'DELETE':
        if delivery_group.user_set.filter(id=id).exists():
            delivery_group.user_set.remove(user)
            return Response({'message': 'User removed from the DeliveryCrew group successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found in the DeliveryCrew group'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def cartCustomerManagement(request):
    if not request.user.groups.exists():
        user = request.user
        if request.method == 'GET':
            cart = models.Cart.objects.filter(user=user)
            serialized_items = serializers.CartSerializer(cart, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serialized_items = serializers.CartSerializer(data=request.data)
            if serialized_items.is_valid():
                menuitem = serialized_items.validated_data['menuitem']
                quantity = serialized_items.validated_data['quantity']
                unit_price = menuitem.price
                total_price = unit_price * quantity
                serialized_items.save(
                    unit_price=unit_price, price=total_price, user=user)
                return Response(serialized_items.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_items.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cart = models.Cart.objects.filter(user=user)
            cart.delete()
            return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response({'message': 'You are a manager or delivery crew. You have to be a customer to order items.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def orderViewManagement(request):
    if not request.user.groups.exists():
        if request.method == 'GET':
            orders = models.Order.objects.filter(user=request.user)

            serialized_orders = serializers.OrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            cart_items = models.Cart.objects.filter(user=request.user)

            if not cart_items.exists():
                return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            total_price = sum(cart_items.price for cart_items in cart_items)

            order = models.Order.objects.create(user=request.user,
                                                total=total_price)

            for cart_item in cart_items:
                order_item = models.OrderItem.objects.create(order=order,
                                                             menuitem=cart_item.menuitem,
                                                             quantity=cart_item.quantity,
                                                             unit_price=cart_item.unit_price,
                                                             price=cart_item.price)

            cart_items.delete()
            return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    elif request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            orders = models.Order.objects.all()

            user_filter = request.query_params.get('user')
            delivery_crew_filter = request.query_params.get('delivery_crew')
            date_filter = request.query_params.get('date')
            status_filter = request.query_params.get('status')
            perpage = request.query_params.get('perpage', default=2)
            page = request.query_params.get('page', default=1)

            if user_filter:
                orders = orders.filter(user__username=user_filter)
            if delivery_crew_filter:
                orders = orders.filter(
                    delivery_crew__username=delivery_crew_filter)
            if date_filter:
                orders = orders.filter(date=date_filter)
            if status_filter:
                orders = orders.filter(status=status_filter)

            paginator = Paginator(orders, per_page=perpage)
            try:
                orders = paginator.page(number=page)
            except EmptyPage:
                orders = []

            serialized_orders = serializers.OrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    elif request.user.groups.filter(name='DeliveryCrew').exists():
        if request.method == 'GET':
            orders = models.Order.objects.filter(delivery_crew=request.user)
            serialized_orders = serializers.OrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def orderItemViewManagement(request, id):
    items = get_object_or_404(models.Order, id=id)

    if not request.user.groups.exists():
        if request.method == 'GET':
            order_items = models.Order.objects.filter(id=id, user=request.user)
            if order_items:
                serialized_order_items = serializers.OrderSerializer(
                    order_items, many=True)
                return Response(serialized_order_items.data, status=status.HTTP_200_OK)
            elif not order_items:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    elif request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            order_items = models.Order.objects.filter(id=id)
            if order_items:
                serialized_order_items = serializers.OrderSerializer(
                    order_items, many=True)
                return Response(serialized_order_items.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        elif request.method in ['PUT', 'PATCH']:
            serialized_order_items = serializers.OrderSerializer(
                items, data=request.data, partial=request.method == 'PATCH')
            if serialized_order_items.is_valid():
                serialized_order_items.save()
                return Response(serialized_order_items.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_order_items.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if items:
                items.delete()
                return Response({'message': 'Order deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    elif request.user.groups.filter(name='DeliveryCrew').exists():
        if request.method == 'PATCH':
            new_status = request.data.get('status')
            if new_status:
                serialized_order = serializers.OrderSerializer(
                    items, data={'status': new_status}, partial=True)

                if serialized_order.is_valid():
                    serialized_order.save()
                    return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response(serialized_order.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Status field is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
