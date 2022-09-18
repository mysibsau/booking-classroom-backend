from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class PersonalStatus(models.IntegerChoices):
    student = 0, "Студент"
    staff = 1, "Сотрудник"


class UserRole(models.IntegerChoices):
    user = 0, "Пользователь"
    admin = 1, "Администратор"
    super_admin = 2, "Супер администратор"


class User(AbstractUser):
    full_mame = models.TextField("ФИО")
    status = models.IntegerField("Статус", choices=PersonalStatus.choices, default=PersonalStatus.student)
    position = models.TextField("Должность/Группа", blank=True, default="", help_text="Должность или группа")
    role = models.IntegerField("Роль", choices=UserRole.choices, default=UserRole.user)

    def __str__(self):
        return self.full_mame


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
