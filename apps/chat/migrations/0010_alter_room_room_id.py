# Generated by Django 5.0.1 on 2024-01-27 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='b43a409e6cc34c2d978b2e508b4649a7', unique=True, verbose_name='Room ID'),
        ),
    ]
