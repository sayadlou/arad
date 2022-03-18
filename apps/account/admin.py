from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


class MyUserAdmin(UserAdmin):
    model = UserProfile


admin.site.register(UserProfile, MyUserAdmin)
