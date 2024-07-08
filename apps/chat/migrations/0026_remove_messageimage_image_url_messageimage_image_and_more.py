# Generated by Django 4.2.10 on 2024-02-14 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0025_alter_room_room_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageimage',
            name='image_url',
        ),
        migrations.AddField(
            model_name='messageimage',
            name='image',
            field=models.FileField(default=1, upload_to='chat/files/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='2b13631d9dcf4a9b987031af2c416d0d', unique=True, verbose_name='Room ID'),
        ),
    ]