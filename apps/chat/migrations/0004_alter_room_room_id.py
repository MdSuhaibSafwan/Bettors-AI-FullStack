# Generated by Django 5.0.1 on 2024-01-27 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='8652beba3130496fb2d7f7bb5f551929', unique=True, verbose_name='ルームID'),
        ),
    ]