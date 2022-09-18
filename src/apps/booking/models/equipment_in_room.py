from django.db import models
from .equipment import Equipment
from .room import Room


class EquipmentInRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Аудитория")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Оборудование")
    count = models.PositiveIntegerField("Кол-во оборудования")

    def __str__(self):
        return str(self.equipment)

    class Meta:
        unique_together = ('room', 'equipment',)
        verbose_name = 'Оборудование в аудитории'
        verbose_name_plural = 'Оборудование в аудитории'
