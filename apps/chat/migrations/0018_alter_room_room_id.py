# Generated by Django 4.2.10 on 2024-02-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_alter_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='9028045eb5224317aad4847b9841f605', unique=True, verbose_name='Room ID'),
        ),
    ]