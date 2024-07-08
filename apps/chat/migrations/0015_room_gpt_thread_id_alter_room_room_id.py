# Generated by Django 4.2.10 on 2024-02-09 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_assistant_room_deleted_at_room_expired_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='gpt_thread_id',
            field=models.CharField(default='th__', help_text='Thread Id of the Assistant', max_length=100, verbose_name='GPT Thread'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='bb4cd0a5351e4b2f84cf396ac72abd25', unique=True, verbose_name='Room ID'),
        ),
    ]
