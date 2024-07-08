# Referrer
# https://qiita.com/kenkono/items/d95aee6e79f671c67aba
from django.db import models
from django.utils import timezone
from encrypted_fields.fields import EncryptedFieldMixin


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass


class EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField):
    pass


class BlockIpList(models.Model):
    ip = EncryptedIPAddressField(
        verbose_name="Blocked IP Address",
        blank=False,
        null=False,
    )
    reason = EncryptedTextField(
        verbose_name="Block Reason",
        blank=True,
        null=True,
    )
    date_create = models.DateTimeField(
        verbose_name="Registration Date and Time",
        blank=False,
        null=False,
        default=timezone.now,
    )

    class Meta:
        app_label = "access_security"
        db_table = "block_ip_list_model"
        verbose_name = verbose_name_plural = "01_Block List"
