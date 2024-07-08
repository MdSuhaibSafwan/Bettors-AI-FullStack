from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from encrypted_fields.fields import (
    SearchField,
    EncryptedTextField,
)
from datetime import datetime, timedelta
from uuid import uuid4

User = get_user_model()


# Temporary registration / official registration function
# Model for issuing TOKEN
class ActivateTokenManager(models.Manager):
    # Email authentication at the time of sign up
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now(),
        ).first()
        # Determine the validity of the authentication URL
        if user_activate_token is None:
            # Delete the invalid Token that was accessed
            user_activate_token = self.filter(token=token)
            if user_activate_token:
                user_activate_token.delete()
            res = False
            msg = "The temporary registration URL has expired. Please sign up again."
            return res, msg
        else:
            user = user_activate_token.user
            user.is_active = True
            user.save()
            res = True
            msg = "Official registration has been completed"
            # Discard the used Token
            user_activate_token.delete()
            return res, msg

    # Email authentication when changing email address
    def activate_change_email_by_token(self, token):
        user_email_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now(),
        ).first()
        # Determine the validity of the authentication URL
        if user_email_activate_token is None:
            # Delete the invalid Token that was accessed
            user_email_activate_token = self.filter(token=token)
            if user_email_activate_token:
                user_email_activate_token.delete()
            res = False
            msg = "The temporary registration URL has expired"
            return res, msg
        else:
            user = user_email_activate_token.user

            if user.is_change_email_request is True:
                user.is_change_email_request = False
                user.save()  # Save the model once in case it is rejected by the same address
                user.email = user.change_email  # Change of email
                user.change_email = "dummy@mail.com"  # Reset the change_email field after authenticating the changed email
                user.save()  # SUCCESS
                res = True
                msg = "The change of email address has been completed\n\
                       Please log in with the changed email address."
                # Discard the used Token
                user_email_activate_token.delete()
                return res, msg
            else:
                # Delete the invalid Token that was accessed
                user_email_activate_token.delete()
                res = False
                msg = "Please change your email address again"
                return res, msg


class ActivateToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # [Memo] CASCADE:親削除->子削除, SET_DEFAULT/SET_NULL:親削除->子保持
        related_name="related_activate_tokens_user",
    )
    _token = EncryptedTextField(
        verbose_name="Token(Encrypted:FormNotUsable)",
        blank=False,
        null=False,
        default=uuid4().hex,
    )
    token = SearchField(
        verbose_name="Token",
        hash_key=settings.ENCRYPTION_HASH_KEY,
        db_index=True,
        unique=True,
        encrypted_field_name="_token",
    )
    expired_at = models.DateTimeField(
        default=datetime.now()
        + timedelta(seconds=settings.EMAIL_CERTIFICATION_TOKEN_AGE),
    )

    objects = ActivateTokenManager()

    def __str__(self):
        return self.user.email

    class Meta:
        app_label = "accounts"
        db_table = "activate_token_model"
        verbose_name = verbose_name_plural = "02_Issue Authentication Token"
