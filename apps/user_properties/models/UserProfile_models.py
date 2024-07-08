from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from common.scripts import validate_bad_id_name_words
from sorl.thumbnail import get_thumbnail, delete

User = get_user_model()


def get_user_icon_image_path(instance, filename):
    return f"apps/user_profile/user_icon/{instance.unique_account_id.pk}/{filename}"


class UserProfile(models.Model):
    staticRoot = (
        settings.STATIC_URL.split("/")[-1]
        if settings.IS_USE_GCS
        else "../" + settings.STATIC_URL
    )
    user_icon_default = staticRoot + "/apps/user_profile/user_icon/default/default.svg"

    unique_account_id = models.OneToOneField(
        User,
        db_index=True,
        primary_key=True,
        on_delete=models.CASCADE,  # [Memo] CASCADE: Parent Delete -> Child Delete, SET_DEFAULT/SET_NULL: Parent Delete -> Child Maintain
        blank=False,
        null=False,
        related_name="related_user_profile_unique_account_id",
        help_text="Associated account ID",
    )
    display_name = models.CharField(
        verbose_name="Display Name",
        default="Enter Name Here",
        max_length=25,
        blank=False,
        null=False,
        unique=False,
        validators=[AbstractUser.username_validator, validate_bad_id_name_words],
        help_text="Alphanumeric, up to 25 characters in length",
    )
    user_icon = models.ImageField(
        verbose_name="Profile Picture",
        upload_to=get_user_icon_image_path,
        blank=False,
        null=False,
        default=user_icon_default,
        help_text=f"Images will be resized to {settings.USER_ICON_RESIZE_HEIGHT}(px) x {settings.USER_ICON_RESIZE_WIDTH}(px)",
    )

    def get_absolute_url(self):
        return self

    def get_subscription(self):
        user = self.unique_account_id
        subscription = user.subscription_set.order_by("-date_create").first()
        if subscription is None:
            return None

        return subscription.name

    def save(self, *args, **kwargs):
        super().save()
        # Resize user_icon image
        try:
            resize_width = settings.USER_ICON_RESIZE_WIDTH
            resize_height = settings.USER_ICON_RESIZE_HEIGHT
            if (
                self.user_icon.width > resize_width
                or self.user_icon.height > resize_height
            ):
                new_width = resize_width
                new_height = resize_height
                resized = get_thumbnail(
                    self.user_icon,
                    f"{new_width}x{new_height}",
                    crop="center",
                    quality=99,
                )
                name = self.user_icon.name.split("/")[-1]

                self.user_icon.save(name, ContentFile(resized.read()), True)
                delete(resized)  # Delete cached file
        except:
            pass  # Avoid processing when user_icon is not present

    class Meta:
        app_label = "user_properties"
        db_table = "user_profile_model"
        verbose_name = verbose_name_plural = "01_User Profile"
