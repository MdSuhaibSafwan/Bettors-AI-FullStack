# Referrer
# https://qiita.com/kin292929/items/92aa0f6f5e1fbca553ee
from django.db import models
from django.conf import settings
from django.utils import timezone
from common.scripts import RequestUtil
from datetime import datetime, timedelta
from encrypted_fields.fields import SearchField, EncryptedFieldMixin, EncryptedCharField


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass


class EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField):
    pass


class AccessSecurityManager(models.Manager):
    @staticmethod
    def insert_access_log(request, type):
        request_util = RequestUtil(request)
        ip = request_util.get_ip()
        # Log entries from the same IP are recorded once every 30 minutes
        logs = AccessSecurity.objects.filter(
            ip=ip,
            type=type,
            date_create__gte=datetime.now() - timedelta(minutes=30),
        ).first()
        if not logs:
            AccessSecurity.objects.create(
                ip=request_util.get_ip(),
                type=type,
                request_host_url=request_util.get_request_host_url(),
            )


class AccessSecurity(models.Model):
    _ip = EncryptedIPAddressField(
        verbose_name="IP Address",
        blank=True,
        null=True,
    )
    ip = SearchField(
        hash_key=settings.ENCRYPTION_HASH_KEY,
        encrypted_field_name="_ip",
    )
    type = models.CharField(
        verbose_name="Type",
        blank=True,
        null=True,
        max_length=256,
    )
    request_host_url = EncryptedTextField(
        verbose_name="Request Host URL",
        blank=True,
        null=True,
    )
    request_url = EncryptedTextField(
        verbose_name="Request URL",
        blank=True,
        null=True,
    )
    user_agent = EncryptedTextField(
        verbose_name="User Agent",
        blank=True,
        null=True,
    )
    csrf_token = EncryptedTextField(
        verbose_name="CSRF Token",
        blank=True,
        null=True,
    )
    time_zone = EncryptedCharField(
        verbose_name="Time Zone",
        blank=True,
        null=True,
        max_length=256,
    )
    date_create = models.DateTimeField(
        verbose_name="Creation Date",
        blank=True,
        null=True,
        default=timezone.now,
    )

    objects = AccessSecurityManager()

    class Meta:
        app_label = "access_security"
        db_table = "access_security_model"
        verbose_name = verbose_name_plural = "02_Block Logs"
