# Generated by Django 4.2.1 on 2024-01-25 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='5820702760574e3b94688fdc51fc721b', unique=True, verbose_name='ルームID'),
        ),
    ]