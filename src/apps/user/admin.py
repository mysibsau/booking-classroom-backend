from django.contrib import admin

from apps.user import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_mame', 'role', )
