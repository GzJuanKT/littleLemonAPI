from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.menuItems.as_view()),
    path('menu-items/<int:pk>', views.menuSingleItem)
]
