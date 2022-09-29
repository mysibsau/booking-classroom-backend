from django.db import models

from .booking import Booking


class BookingDateTime(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_date_time")
    date_start = models.DateField("Дата начала бронирования")
    date_end = models.DateField("Дата конца бронирования")
    start_time = models.TimeField("Время начала брони", null=True, blank=True)
    end_time = models.TimeField("Время конца брони", null=True, blank=True)

    def __str__(self):
        if self.date_start == self.date_end:
            return f"{self.date_start.strftime('%d-%m-%Y')}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        return f"{self.date_start.strftime('%d-%m-%Y')} -- {self.date_end.strftime('%d-%m-%Y')}"

    class Meta:
        verbose_name = 'Даты и время брони'
        verbose_name_plural = 'Даты и время брони'
