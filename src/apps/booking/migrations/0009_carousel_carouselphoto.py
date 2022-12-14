# Generated by Django 3.2.7 on 2022-09-22 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_alter_room_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec_text', models.TextField(verbose_name='Заголовок на сайте')),
            ],
        ),
        migrations.CreateModel(
            name='CarouselPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images/', verbose_name='Фотография')),
                ('address', models.TextField(verbose_name='В какой аудитории сделана фотография')),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_photo', to='booking.carousel', verbose_name='rules')),
            ],
        ),
    ]
