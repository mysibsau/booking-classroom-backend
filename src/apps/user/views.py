import requests

from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as StandartObtainAuthToken
from rest_framework.response import Response

from .serializers import AuthTokenSerializer
from .models import User


class ObtainAuthToken(StandartObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "role": user.role,
                    "name": user.full_name,
                    "id": user.id,
                }
            )
        response, status_code = self.__check_user(request)
        return Response(response, status=status_code)

    def __check_user(self, request):
        base_url = settings.AUTH_URL
        session = requests.session()
        auth = session.post(
            url=f"{base_url}/login/",
            json={
                "login": request.data['username'],
                "password": request.data['password']
                },
            headers=settings.AUTH_HEADERS
        )
        if auth.status_code == 200:
            full_name = session.post(
                url=f"{base_url}/me",
                params={
                    "token": auth.json()['token']
                },
                headers=settings.AUTH_HEADERS
            )
            user = User.objects.create(
                full_name=full_name.json()['full_name'],
                username=request.data['username']
            )
            user.set_password(request.data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return {
                    "token": token.key,
                    "role": user.role,
                    "name": user.full_name,
                    "id": user.id,
                }, 200

        return {"detail": "Неверный логин или пароль"}, 401


obtain_auth_token = ObtainAuthToken.as_view()
