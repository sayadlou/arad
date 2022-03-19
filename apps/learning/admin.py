from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Post, VideoFile
from .views import refresh


@admin.register(Category)
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug']
    readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}
