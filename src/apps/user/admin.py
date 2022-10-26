from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'username')
    list_display = ('username', 'full_name', 'role', )
    exclude = (
        'password',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'last_login',
        'user_permissions',
        'username'
    )
