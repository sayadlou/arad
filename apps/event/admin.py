from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Organizer, Event, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 2
    readonly_fields = ['id']


class OrganizerInLine(admin.TabularInline):
    model = Organizer


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    readonly_fields = ['id']
    inlines = [OrganizerInLine]
    prepopulated_fields = {'slug': ('title',)}
