from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem, OrderItem, Order, Product


class CartItemInLine(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner']
    readonly_fields = ['id']
    inlines = [CartItemInLine]


#
# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     search_fields = ['cart']
#     list_display = ['cart', 'product']
#     readonly_fields = ['id']


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner', ]
    readonly_fields = ['id']
    inlines = [OrderItemInLine]


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     search_fields = ['order']
#     list_display = ['order', 'product']
#     readonly_fields = ['id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
