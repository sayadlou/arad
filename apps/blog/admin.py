from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
