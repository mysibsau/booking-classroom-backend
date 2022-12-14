from django.db import models
from django.conf import settings
from PIL import Image

from .equipment import Equipment


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    admin = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Администратор",
        related_name="room_admin"
    )
    pseudo_admins = models.ManyToManyField(
        User,
        verbose_name="Доп. администраторы",
        null=True,
        blank=True,
    )
    description = models.TextField("Описание")
    address = models.TextField("Адрес")
    capacity = models.PositiveIntegerField("Вместимость")
    equipment = models.ManyToManyField(Equipment, through='EquipmentInRoom', verbose_name="Оборудование в аудитории")
    admin_contact_info = models.TextField('Контактная информация администратора', null=True, blank=True)

    def __str__(self):
        return f"{self.address}"

    class Meta:
        verbose_name = 'Аудитории'
        verbose_name_plural = 'Аудитории'


class RoomPhoto(models.Model):
    room = models.ForeignKey(
        Room,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Аудитория",
        related_name="room_photo"
    )
    photo = models.ImageField("Фотография", upload_to="images/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        output_size = (1280, 720)
        img.thumbnail(output_size)
        img.save(self.photo.path)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
