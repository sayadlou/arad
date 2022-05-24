from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    list_display = ['title',]
    readonly_fields = ['id']
    exclude = ('slug',)
