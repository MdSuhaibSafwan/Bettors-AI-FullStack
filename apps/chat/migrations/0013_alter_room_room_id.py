# Generated by Django 5.0.2 on 2024-02-08 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='3bc4dfc528f34b459c91ac4c0e69f7ef', unique=True, verbose_name='Room ID'),
        ),
    ]
