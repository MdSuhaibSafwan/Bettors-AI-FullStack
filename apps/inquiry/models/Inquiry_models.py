from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from encrypted_fields.fields import (
    EncryptedFieldMixin,
    SearchField,
    EncryptedEmailField,
)
from .Inquiry_ChoiceList import SITUATION_CHOICES_LIST

User = get_user_model()
SITUATION_CHOICES_LIST = SITUATION_CHOICES_LIST()


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass


class EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField):
    pass


class Inquiry(models.Model):
    unique_account_id = models.ForeignKey(
        User,
        db_index=False,
        primary_key=False,
        on_delete=models.SET_NULL,  # [Memo] CASCADE: Parent deletion, child deletion, SET_DEFAULT/SET_NULL: Parent deletion, child retention
        blank=True,
        null=True,
        related_name="related_inquiry_unique_account_id",
        help_text="Associated Account ID",
    )
    _email = EncryptedEmailField(
        verbose_name="Email Address (Encrypted: Not for form use)",
        blank=False,
        null=False,
        max_length=255,
    )
    email = SearchField(
        verbose_name="Email Address",
        hash_key=settings.ENCRYPTION_HASH_KEY,
        db_index=False,
        unique=False,
        help_text="Depending on the content, we may contact you regarding the inquiry",
        encrypted_field_name="_email",
    )
    _inquiry_text = EncryptedTextField(
        verbose_name="Inquiry Text (Encrypted: Not for form use)",
        blank=False,
        null=False,
        max_length=2000,
    )
    inquiry_text = SearchField(
        verbose_name="Inquiry Text",
        hash_key=settings.ENCRYPTION_HASH_KEY,
        db_index=False,
        unique=False,
        encrypted_field_name="_inquiry_text",
    )
    date_create = models.DateTimeField(
        verbose_name="Inquiry Date and Time",
        default=timezone.now,
    )
    _ip_address = EncryptedIPAddressField(
        verbose_name="Inquirer IP Address (Encrypted: Not for form use)",
        blank=True,
        null=True,
    )
    ip_address = SearchField(
        verbose_name="Inquirer IP Address",
        hash_key=settings.ENCRYPTION_HASH_KEY,
        db_index=False,
        unique=False,
        encrypted_field_name="_ip_address",
    )
    situation = models.IntegerField(
        verbose_name="Status",
        blank=False,
        null=False,
        choices=SITUATION_CHOICES_LIST,
        default=0,
    )
    date_complete = models.DateTimeField(
        verbose_name="Completion Date and Time",
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        app_label = "inquiry"
        db_table = "inquiry_model"
        verbose_name = verbose_name_plural = "Inquiry List"
