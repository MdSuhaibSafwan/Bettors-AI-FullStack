# Generated by Django 5.0.1 on 2024-01-27 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='982578e8a1d5401db5e9047db84237e0', unique=True, verbose_name='Room ID'),
        ),
    ]
