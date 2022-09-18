from django.db import models

from .booking import Booking


class BookingDateTime(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_date_time")
    date = models.DateField("Дата бронирования")
    start_time = models.TimeField("Время начала брони")
    end_time = models.TimeField("Время конца брони")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = 'Даты и время брони'
        verbose_name_plural = 'Даты и время брони'
