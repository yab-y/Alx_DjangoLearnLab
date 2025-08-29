# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("id", "username", "email", "is_staff")
    filter_horizontal = ("following",)  # shows the M2M widget in admin
