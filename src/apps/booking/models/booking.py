from django.db import models
from django.conf import settings

from .room import Room


User = settings.AUTH_USER_MODEL


class PersonalStatus(models.IntegerChoices):
    student = 0, "Студент"
    staff = 1, "Сотрудник"


class BookingStatus(models.IntegerChoices):
    in_process = 0, "В обработке"
    rejected = 1, "Отклонено"
    accepted = 2, "Одобрено"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    contact_info = models.TextField("Контактная информация")
    equipment = models.TextField("Забронированное оборудование", blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Аудитория", related_name="bookings_in_room")
    title = models.TextField('Название мероприятия')
    description = models.TextField("Описание")
    status = models.IntegerField("Статус заявки", choices=BookingStatus.choices, default=BookingStatus.in_process)
    comment = models.TextField("Ваш комментарий", blank=True, null=True)
    personal_status = models.IntegerField("Статус", choices=PersonalStatus.choices, default=PersonalStatus.student)
    position = models.TextField("Должность/Группа", blank=True, default="", help_text="Должность или группа")
    created_at = models.DateTimeField("Дата создания заявки", auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user}, {self.room}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
