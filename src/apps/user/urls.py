from django.urls import path

from .views import obtain_auth_token


user_urls = [
    path("auth/", obtain_auth_token),
]
