# Generated by Django 3.2.7 on 2023-03-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0021_alter_booking_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания заявки'),
        ),
    ]
