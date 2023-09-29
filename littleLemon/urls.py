from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login_api'),
    path('log-in/', views.login_view, name='logintemplate_api'),
    path('test_token/', views.test_token, name='tokentest_api'),
    path('all_users/', views.all_users, name='allusers_api'),
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.menuItems.as_view()),
    path('menu-items/<int:pk>', views.menuSingleItem),
    path('groups/manager/users', views.listAddUsersManagerGroup),
    path('groups/manager/users/<int:id>', views.removeUserManagerGroup),
    path('groups/delivery-crew/users', views.listAddUsersDeliveryCrewGroup),
    path('groups/delivery-crew/users/<int:id>',
         views.removeUserDeliveryCrewGroup),
    path('cart/menu-items', views.cartCustomerManagement),
    path('orders', views.orderViewManagement),
    path('orders/<int:id>', views.orderItemViewManagement),
]
