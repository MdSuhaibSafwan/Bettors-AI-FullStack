# Generated by Django 4.2.1 on 2024-01-25 16:35

import apps.inquiry.models.Inquiry_models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import encrypted_fields.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "_email",
                    encrypted_fields.fields.EncryptedEmailField(
                        max_length=255,
                        verbose_name="Email Address (Encrypted: Not for form use)",
                    ),
                ),
                (
                    "email",
                    encrypted_fields.fields.SearchField(
                        blank=True,
                        db_index=True,
                        encrypted_field_name="_email",
                        hash_key="***YOUR_ENCRYPTION_HASH_KEY***",
                        help_text="Depending on the content, we may contact you regarding the inquiry",
                        max_length=66,
                        null=True,
                        verbose_name="Email Address",
                    ),
                ),
                (
                    "_inquiry_text",
                    apps.inquiry.models.Inquiry_models.EncryptedTextField(
                        max_length=2000,
                        verbose_name="Inquiry Text (Encrypted: Not for form use)",
                    ),
                ),
                (
                    "inquiry_text",
                    encrypted_fields.fields.SearchField(
                        blank=True,
                        db_index=True,
                        encrypted_field_name="_inquiry_text",
                        hash_key="***YOUR_ENCRYPTION_HASH_KEY***",
                        max_length=66,
                        null=True,
                        verbose_name="Inquiry Text",
                    ),
                ),
                (
                    "date_create",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Inquiry Date and Time",
                    ),
                ),
                (
                    "_ip_address",
                    apps.inquiry.models.Inquiry_models.EncryptedIPAddressField(
                        blank=True,
                        null=True,
                        verbose_name="Inquirer IP Address (Encrypted: Not for form use)",
                    ),
                ),
                (
                    "ip_address",
                    encrypted_fields.fields.SearchField(
                        blank=True,
                        db_index=True,
                        encrypted_field_name="_ip_address",
                        hash_key="***YOUR_ENCRYPTION_HASH_KEY***",
                        max_length=66,
                        null=True,
                        verbose_name="Inquirer IP Address",
                    ),
                ),
                (
                    "situation",
                    models.IntegerField(
                        choices=[
                            (0, "Unresolved"),
                            (11, "Investigating"),
                            (12, "Confirming with Inquirer"),
                            (13, "Confirming with Stakeholders"),
                            (80, "Other Ongoing"),
                            (90, "Completed"),
                        ],
                        default=0,
                        verbose_name="Status",
                    ),
                ),
                (
                    "date_complete",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Completion Date and Time",
                    ),
                ),
                (
                    "unique_account_id",
                    models.ForeignKey(
                        blank=True,
                        db_index=False,
                        help_text="Associated Account ID",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="related_inquiry_unique_account_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Inquiry List",
                "verbose_name_plural": "Inquiry List",
                "db_table": "inquiry_model",
            },
        ),
    ]
