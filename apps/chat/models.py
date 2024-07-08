from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q
from uuid import uuid4
from .settings import (
    MaxSystemSentence,
    MaxAssistantSentence,
    MaxHistoryLen,
    MinTokens,
    MaxTokens,
)
from .managers import AssistantManager, RoomManager

User = get_user_model()


def get_ai_icon_image_path(instance, filename):
    return f"apps/chat/ai_icon/{instance.room_id.pk}/{filename}"


class Assistant(models.Model):
    name = models.CharField(max_length=200)
    model_id = models.CharField(max_length=200)
    default = models.BooleanField(default=False)
    instructions = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = AssistantManager()


class AssistantFunction(models.Model):
    assistant = models.ManyToManyField(Assistant)
    function_name = models.CharField(max_length=200)
    endpoint = models.URLField()
    openapi_schema = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.function_name


class Room(models.Model):
    room_id = models.SlugField(
        verbose_name="Room ID",
        db_index=True,
        unique=True,
        blank=False,
        null=False,
        default=uuid4().hex,
    )
    create_user = models.ForeignKey(
        User,
        verbose_name="Creator",
        on_delete=models.CASCADE,  # [Memo] CASCADE: Parent deletion, child deletion, SET_DEFAULT/SET_NULL: Parent deletion, child retention
        blank=False,
        null=False,
        related_name="related_room_model_create_user",
        help_text="Associated Account ID",
    )
    assistant_used = models.ForeignKey(
        Assistant, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Assistant",
        help_text="Assistant Getting used in a Room"
    )
    gpt_thread_id = models.CharField(
        max_length=100,
        verbose_name="GPT Thread",
        help_text="Thread Id of the Assistant",
    )
    date_create = models.DateTimeField(
        verbose_name="Creation Date and Time",
        default=timezone.now,
        help_text="Creation Date and Time",
    )

    expired_at = models.DateTimeField(
        verbose_name="Expiration Date and Time",
        help_text="Expiration Time of a Thread/Room",
        null=True, 
        blank=True
    )
    deleted_at = models.DateTimeField(
        verbose_name="Deletion Date and Time",
        help_text="Deletion Time of a Thread/Room",
        null=True, 
        blank=True
    )

    objects = RoomManager()

    class Meta:
        app_label = "chat"
        db_table = "room_model"
        verbose_name = verbose_name_plural = "Room List"

    def check_expired(self):
        _expired = False
        if self.expired_at: 
            _expired = True
            return _expired

        now = timezone.now()
        timedelt = now - self.date_create
        del_hours = float((timedelt.seconds / 60) / 60)
        if del_hours >= float(1):
            if not _expired:
                self.expired_at = timezone.now()
                self.save()
                _expired = True

            return _expired

        return _expired

    def get_first_message_content(self):
        message_obj = self.chatmessage_set.first()
        if message_obj is None:
            return "New Chat"
        return message_obj.user_message


class RoomSettings(models.Model):
    staticRoot = (
        settings.STATIC_URL.split("/")[-1]
        if settings.IS_USE_GCS
        else "../" + settings.STATIC_URL
    )
    ai_icon_default = staticRoot + "/apps/chat/ai_icon/default/ai.png"

    room_id = models.OneToOneField(
        Room,
        verbose_name="Room ID",
        db_index=True,
        on_delete=models.CASCADE,  # [Memo] CASCADE: Parent deletion, child deletion, SET_DEFAULT/SET_NULL: Parent deletion, child retention
        blank=False,
        null=False,
        related_name="related_room_settings_model_room_id",
        help_text="Associated Room ID",
    )
    room_name = models.CharField(
        verbose_name="Room Name",
        default="NewChatRoom",
        max_length=50,
        blank=False,
        null=False,
        unique=False,
        help_text="Alphanumeric characters up to 50 characters in length",
    )
    ai_icon = models.ImageField(
        verbose_name="AI Icon",
        upload_to=get_ai_icon_image_path,
        blank=False,
        null=False,
        default=ai_icon_default,
        help_text=f"Images will be resized to {settings.USER_ICON_RESIZE_HEIGHT}px x {settings.USER_ICON_RESIZE_WIDTH}px",
    )
    system_sentence = models.TextField(
        verbose_name="System Message",
        max_length=MaxSystemSentence,
        blank=True,
        null=True,
        default="",
        help_text=f"Maximum {MaxSystemSentence} characters",
    )
    assistant_sentence = models.TextField(
        verbose_name="Assistant Message",
        max_length=MaxAssistantSentence,
        blank=True,
        null=True,
        default="",
        help_text=f"Maximum {MaxAssistantSentence} characters",
    )
    history_len = models.IntegerField(
        verbose_name="History Length",
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(MaxHistoryLen)],
        help_text=f"Number of recent conversations to include in history (up to {MaxHistoryLen})",
    )
    max_tokens = models.IntegerField(
        verbose_name="Maximum Tokens",
        blank=False,
        null=False,
        default=256,
        validators=[MinValueValidator(MinTokens), MaxValueValidator(MaxTokens)],
        help_text=f"Maximum length of generated tokens (up to {MaxTokens})",
    )
    temperature = models.FloatField(
        verbose_name="Temperature",
        blank=False,
        null=False,
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text="Randomness of generated text (between 0 and 2)",
    )
    top_p = models.FloatField(
        verbose_name="Top P",
        blank=False,
        null=False,
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Word selection selectivity (between 0 and 1)",
    )
    presence_penalty = models.FloatField(
        verbose_name="Presence Penalty",
        blank=False,
        null=False,
        default=1.0,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
        help_text="Penalty for already mentioned words (between -2 and 2)",
    )
    frequency_penalty = models.FloatField(
        verbose_name="Frequency Penalty",
        blank=False,
        null=False,
        default=1.0,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
        help_text="Penalty for the frequency of already mentioned words (between -2 and 2)",
    )
    comment = models.TextField(
        verbose_name="Comment/Note",
        blank=True,
        null=True,
        max_length=256,
        default="",
        help_text="Alphanumeric characters up to 256 characters in length",
    )

    class Meta:
        app_label = "chat"
        db_table = "room_settings_model"
        verbose_name = verbose_name_plural = "Room Settings"


# Room 作成と同時に RoomSettings を作成
@receiver(post_save, sender=Room)
def create_related_model_for_custom_user_model(sender, instance, created, **kwargs):
    # Only execute when a new Room model is created
    if created:
        # Create a record if it doesn't exist, or return the existing record
        _ = RoomSettings.objects.get_or_create(room_id=instance)


@receiver(signal=post_save, sender=Room)
def make_the_previous_rooms_expire(sender, instance, created, **kwargs):
    if created:
        qs = Room.objects.filter(~Q(id=instance.id), expired_at=None)
        qs.update(expired_at=timezone.now())


class Message(models.Model):
    room_id = models.ForeignKey(
        Room,
        verbose_name="Room ID",
        db_index=True,
        on_delete=models.CASCADE,  # [Memo] CASCADE: Parent deletion, child deletion, SET_DEFAULT/SET_NULL: Parent deletion, child retention
        blank=False,
        null=False,
        related_name="related_message_model_room_id",
        help_text="Associated Room ID",
    )
    user_message = models.TextField(
        verbose_name="User Message",
        blank=True,
        null=True,
    )
    user_settings = models.TextField(
        verbose_name="User's LLM Settings",
        blank=True,
        null=True,
    )
    llm_response = models.TextField(
        verbose_name="LLM Response",
        blank=True,
        null=True,
    )
    response_info = models.TextField(
        verbose_name="Additional Information",
        blank=True,
        null=True,
    )
    date_create = models.DateTimeField(
        verbose_name="Creation Date and Time",
        default=timezone.now,
        help_text="Creation Date and Time",
    )

    class Meta:
        app_label = "chat"
        db_table = "message_model"
        verbose_name = verbose_name_plural = "Message List"


class MessageImage(models.Model):
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name="images",
        help_text="Image for any Message",
    )
    image_url = models.CharField(max_length=20400, verbose_name="Image URL of a Message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = "chat"
        db_table = "message_image_model"
        verbose_name = verbose_name_plural = "Message Images"

