# Generated by Django 3.2.7 on 2022-09-28 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'Пользователь'), (1, 'Администратор'), (2, 'Супер администратор'), (3, 'Доп. администратор')], default=0, verbose_name='Роль'),
        ),
    ]
