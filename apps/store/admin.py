from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *
from .views import refresh


class CartItemInLine(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner']
    readonly_fields = ['id']
    inlines = [CartItemInLine]


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner', ]
    readonly_fields = ['id']
    inlines = [OrderItemInLine]


@admin.register(ProductBaseModel)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceCategory)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2
    readonly_fields = ['id']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
    # search_fields = ['title']
    # list_display = ['title']
    # readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(LearningCategory)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2
    readonly_fields = ['id']


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    readonly_fields = ['id']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url("refresh/", refresh)
        ]
        return my_urls + urls


@admin.register(LearningPost)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug']
    readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(EventCategory)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2
    readonly_fields = ['id']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # search_fields = ['title']
    # list_display = ['title']
    # readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}