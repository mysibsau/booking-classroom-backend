from django.db import models

from .room import Room


class StaticDateTime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="static_date_time")
    date_start = models.DateField("Дата начала бронирования", null=True)
    date_end = models.DateField("Дата конца бронирования", null=True)
    start_time = models.TimeField("Время начала брони")
    end_time = models.TimeField("Время конца брони")
    comment = models.TextField("Для кого данная бронь")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = 'Даты и время для запрета бронирования'
        verbose_name_plural = 'Даты и время запрета бронирования'
