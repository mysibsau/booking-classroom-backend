# Generated by Django 3.2.7 on 2022-09-28 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_full_mame_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'Пользователь'), (1, 'Администратор'), (2, 'Супер администратор'), (3, 'Псевдо-администратор')], default=0, verbose_name='Роль'),
        ),
    ]
