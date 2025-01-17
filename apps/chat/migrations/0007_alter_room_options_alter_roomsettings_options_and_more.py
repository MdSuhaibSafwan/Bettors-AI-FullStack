# Generated by Django 5.0.1 on 2024-01-27 22:22

import apps.chat.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_room_room_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Room List', 'verbose_name_plural': 'Room List'},
        ),
        migrations.AlterModelOptions(
            name='roomsettings',
            options={'verbose_name': 'Room Settings', 'verbose_name_plural': 'Room Settings'},
        ),
        migrations.AlterField(
            model_name='room',
            name='create_user',
            field=models.ForeignKey(help_text='Associated Account ID', on_delete=django.db.models.deletion.CASCADE, related_name='related_room_model_create_user', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='room',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Creation Date and Time', verbose_name='Creation Date and Time'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.SlugField(default='4e624935b089478a955cbb4791c05e62', unique=True, verbose_name='Room ID'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='ai_icon',
            field=models.ImageField(default='..//static//apps/chat/ai_icon/default/ai.png', help_text='Images will be resized to 400px x 400px', upload_to=apps.chat.models.get_ai_icon_image_path, verbose_name='AI Icon'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='assistant_sentence',
            field=models.TextField(blank=True, default='', help_text='Maximum 1500 characters', max_length=1500, null=True, verbose_name='Assistant Message'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='comment',
            field=models.TextField(blank=True, default='', help_text='Alphanumeric characters up to 256 characters in length', max_length=256, null=True, verbose_name='Comment/Note'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='frequency_penalty',
            field=models.FloatField(default=1.0, help_text='Penalty for the frequency of already mentioned words (between -2 and 2)', validators=[django.core.validators.MinValueValidator(-2), django.core.validators.MaxValueValidator(2)], verbose_name='Frequency Penalty'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='history_len',
            field=models.IntegerField(default=0, help_text='Number of recent conversations to include in history (up to 30)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)], verbose_name='History Length'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='max_tokens',
            field=models.IntegerField(default=256, help_text='Maximum length of generated tokens (up to 2048)', validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(2048)], verbose_name='Maximum Tokens'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='presence_penalty',
            field=models.FloatField(default=1.0, help_text='Penalty for already mentioned words (between -2 and 2)', validators=[django.core.validators.MinValueValidator(-2), django.core.validators.MaxValueValidator(2)], verbose_name='Presence Penalty'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='room_id',
            field=models.OneToOneField(help_text='Associated Room ID', on_delete=django.db.models.deletion.CASCADE, related_name='related_room_settings_model_room_id', to='chat.room', verbose_name='Room ID'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='room_name',
            field=models.CharField(default='NewChatRoom', help_text='Alphanumeric characters up to 50 characters in length', max_length=50, verbose_name='Room Name'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='system_sentence',
            field=models.TextField(blank=True, default='', help_text='Maximum 1500 characters', max_length=1500, null=True, verbose_name='System Message'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='temperature',
            field=models.FloatField(default=1.0, help_text='Randomness of generated text (between 0 and 2)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='Temperature'),
        ),
        migrations.AlterField(
            model_name='roomsettings',
            name='top_p',
            field=models.FloatField(default=1.0, help_text='Word selection selectivity (between 0 and 1)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Top P'),
        ),
    ]
