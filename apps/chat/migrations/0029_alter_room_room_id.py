# Generated by Django 4.2.10 on 2024-02-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0028_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='1f189d289969462398e5a394c8f8b399', unique=True, verbose_name='Room ID'),
        ),
    ]
