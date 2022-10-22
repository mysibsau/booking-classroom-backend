from django.contrib import admin

from apps.user import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', )
    readonly_fields = ('full_name', )
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
