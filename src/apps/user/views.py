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
        response = self.__check_user(request)
        return Response(response)

    def __check_user(self, request):
        base_url = settings.AUTH_URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1'
        }
        session = requests.session()
        auth = session.post(
            url=f"{base_url}/login/",
            json={
                "login": request.data['username'],
                "password": request.data['password']
                },
            headers=headers
        )
        if auth.status_code == 200:
            full_name = requests.post(
                url=f"{base_url}/me",
                params={
                    "token": auth.json()['token']
                }
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
                }
        return {
            "status_code": auth
        }


obtain_auth_token = ObtainAuthToken.as_view()
