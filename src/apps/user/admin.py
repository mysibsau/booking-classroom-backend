from django.contrib import admin

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

    def get_search_results(self, request, queryset, search_term):
        path = request.get_full_path_info()
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term, )
        if path == '/admin/autocomplete/?app_label=booking&model_name=room&field_name=admin':
            queryset = queryset.exclude(role__in=[0, 3])
            return queryset, may_have_duplicates

        elif path == '/admin/autocomplete/?app_label=booking&model_name=room&field_name=pseudo_admins':
            queryset = queryset.exclude(role__in=[0, 1, 2])
            return queryset, may_have_duplicates

        return queryset, may_have_duplicates
