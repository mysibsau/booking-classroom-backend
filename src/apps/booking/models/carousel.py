from django.db import models


class Carousel(models.Model):
    spec_text = models.TextField('Заголовок на сайте')

    def __str__(self):
        return "Текст и фотографии для главной страницы"

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'


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
