from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Columns shown in the user list
    list_display = ('username', 'email', 'phone', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone')

    # Add our custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone')}),
    )