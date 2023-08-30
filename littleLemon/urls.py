from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.menuItems.as_view()),
    path('menu-items/<int:pk>', views.menuSingleItem),
    path('groups/manager/users', views.listAddUsersManagerGroup),
    path('groups/manager/users/<int:id>', views.removeUserManagerGroup),
    path('groups/delivery-crew/users', views.listAddUsersDeliveryCrewGroup),
    path('groups/delivery-crew/users/<int:id>',
         views.removeUserDeliveryCrewGroup),
]
