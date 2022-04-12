from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Event, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2
    readonly_fields = ['id']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    # search_fields = ['title']
    # list_display = ['title']
    # readonly_fields = ['id']
    # prepopulated_fields = {'slug': ('title',)}
