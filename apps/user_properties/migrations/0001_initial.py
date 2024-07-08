# Generated by Django 4.2.1 on 2024-01-25 16:35

import apps.user_properties.models.UserProfile_models
import common.scripts.custom_validaters
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0002_alter_activatetoken__token_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "unique_account_id",
                    models.OneToOneField(
                        help_text="Associated account ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="related_user_profile_unique_account_id",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        default="Not set",
                        help_text="Up to 25 alphanumeric characters",
                        max_length=25,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator(),
                            common.scripts.custom_validaters.validate_bad_id_name_words,
                        ],
                        verbose_name="Display Name",
                    ),
                ),
                (
                    "user_icon",
                    models.ImageField(
                        default="..//static//apps/user_profile/user_icon/default/default.svg",
                        help_text="Images will be resized to 400x400 pixels",
                        upload_to=apps.user_properties.models.UserProfile_models.get_user_icon_image_path,
                        verbose_name="Profile Picture",
                    ),
                ),
            ],
            options={
                "verbose_name": "01_User Profile",
                "verbose_name_plural": "01_User Profiles",
                "db_table": "user_profile_model",
            },
        ),
        migrations.CreateModel(
            name="UserReceptionSetting",
            fields=[
                (
                    "unique_account_id",
                    models.OneToOneField(
                        help_text="Associated account ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="related_user_reception_setting_unique_account_id",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "is_receive_all",
                    models.BooleanField(
                        default=True, verbose_name="Receive all notifications"
                    ),
                ),
                (
                    "is_receive_important_only",
                    models.BooleanField(
                        default=False,
                        verbose_name="Receive only important notifications",
                    ),
                ),
            ],
            options={
                "verbose_name": "90_Email Reception Settings",
                "verbose_name_plural": "90_Email Reception Settings",
                "db_table": "user_reception_setting_model",
            },
        ),
    ]
