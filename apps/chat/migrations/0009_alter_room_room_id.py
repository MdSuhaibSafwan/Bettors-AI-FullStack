# Generated by Django 5.0.1 on 2024-01-27 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='e635c937d73843d4bbc5201a089bbbd9', unique=True, verbose_name='Room ID'),
        ),
    ]
