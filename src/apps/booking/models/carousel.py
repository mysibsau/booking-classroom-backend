from django.db import models
from PIL import Image


class Carousel(models.Model):
    title = models.TextField("Заголовок правил")
    spec_text = models.TextField('Правила')
    pseudo_text_booking = models.TextField('Описание заявки')
    pseudo_text_equipment = models.TextField('Описание оборудования')

    def __str__(self):
        return "Общие настройки сайта"

    class Meta:
        verbose_name = 'Общие настройки сайта'
        verbose_name_plural = 'Общие настройки сайта'


class CarouselPhoto(models.Model):
    carousel = models.ForeignKey(
        Carousel,
        on_delete=models.CASCADE,
        verbose_name="rules",
        related_name="carousel_photo"
    )
    photo = models.ImageField("Фотография", upload_to="carousel_images/")
    address = models.CharField("В какой аудитории сделана фотография", max_length=128)
    event = models.TextField("Название мероприятия")

    def __str__(self):
        return "Фотографии в карусели"

    class Meta:
        verbose_name = 'Фотографии в карусели'
        verbose_name_plural = 'Фотографии в карусели'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        output_size = (1280, 720)
        img.thumbnail(output_size)
        img.save(self.photo.path)
