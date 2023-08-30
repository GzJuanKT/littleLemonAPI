from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from rest_framework import permissions

from rest_framework.throttling import UserRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User, Group

from . import models
from . import serializers

from django.shortcuts import get_object_or_404
# Create your views here.


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
