# Generated by Django 4.2.10 on 2024-02-12 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='4fce56f3dedb46d8affd30996602acfc', unique=True, verbose_name='Room ID'),
        ),
    ]
