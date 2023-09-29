from django.contrib import admin
from . import models
from django.contrib.auth.models import User

# Register your models here.


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'featured', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity', 'unit_price', 'price')
    list_filter = ('user', 'menuitem')
    search_fields = ('user__username', 'menuitem__title')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_crew', 'status', 'total', 'date')
    list_filter = ('user', 'status', 'date', 'delivery_crew')
    search_fields = ('user__username', 'delivery_crew__title')


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'unit_price', 'price')
    list_filter = ('order', 'menuitem')
    search_fields = ('order__user__username', 'menuitem__title')


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemsAdmin)
