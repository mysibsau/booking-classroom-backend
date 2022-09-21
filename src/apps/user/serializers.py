from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerDefault

from apps.user.models import User, UserRole


class AuthTokenSerializer(AuthTokenSerializerDefault):
    id = serializers.IntegerField(label="ID", read_only=True)
    full_name = serializers.CharField(label="ФИО пользователя", read_only=True)
    role = serializers.ChoiceField(label="Роль пользователя", read_only=True, choices=UserRole.choices)
