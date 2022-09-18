from django.db import models


class Equipment(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
