from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRole(models.IntegerChoices):
    user = 0, "Пользователь"
    admin = 1, "Администратор"
    super_admin = 2, "Супер администратор"
    pseudo_admin = 3, "Доп. администратор"


class User(AbstractUser):
    full_name = models.TextField("ФИО")
    role = models.IntegerField("Роль", choices=UserRole.choices, default=UserRole.user)

    def __str__(self):
        if self.full_name == '-':
            return self.username
        return self.full_name


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
