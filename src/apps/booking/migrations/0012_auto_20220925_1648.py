# Generated by Django 3.2.7 on 2022-09-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_alter_booking_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingdatetime',
            name='date',
        ),
        migrations.AddField(
            model_name='bookingdatetime',
            name='date_end',
            field=models.DateField(null=True, verbose_name='Дата конца бронирования'),
        ),
        migrations.AddField(
            model_name='bookingdatetime',
            name='date_start',
            field=models.DateField(null=True, verbose_name='Дата начала бронирования'),
        ),
    ]
