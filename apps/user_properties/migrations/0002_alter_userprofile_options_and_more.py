# Generated by Django 5.0.1 on 2024-01-27 22:03

import apps.user_properties.models.UserProfile_models
import common.scripts.custom_validaters
import django.contrib.auth.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_properties', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '01_User Profile', 'verbose_name_plural': '01_User Profile'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(default='Not Set', help_text='Alphanumeric, up to 25 characters in length', max_length=25, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), common.scripts.custom_validaters.validate_bad_id_name_words], verbose_name='Display Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='unique_account_id',
            field=models.OneToOneField(help_text='Associated account ID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='related_user_profile_unique_account_id', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_icon',
            field=models.ImageField(default='..//static//apps/user_profile/user_icon/default/default.svg', help_text='Images will be resized to 400(px) x 400(px)', upload_to=apps.user_properties.models.UserProfile_models.get_user_icon_image_path, verbose_name='Profile Picture'),
        ),
    ]
