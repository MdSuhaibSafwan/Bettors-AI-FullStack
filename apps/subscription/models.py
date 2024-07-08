from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db.models import Q
from dateutil import relativedelta
from django.utils import timezone
from apps.chat.models import Message

User = get_user_model()


class SubscriptionManager(models.Manager):

    def get_default_free_subscription(self):
        qs = self.get_free_subscriptions()
        return qs.first()

    def get_free_subscriptions(self):
        qs = self.get_queryset().filter(price=float(0))
        return qs

    def get_paid_subscriptions(self):
        qs = self.get_queryset().filter(~Q(price=float(0)))
        return qs


class Subscription(models.Model):
    SUBSCRIPTION_TYPE = (
        ("mn", "Monthly"),
        ("yr", "Yearly"),
        ("wk", "Weekly"),
    )
    SUBSCRIPTION_DAYS = {
        "yr": relativedelta.relativedelta(years=+1),
        "mn": relativedelta.relativedelta(months=+1),
        "wk": relativedelta.relativedelta(days=+7)
    }
    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    user = models.ManyToManyField(
        User, 
        through="UserSubscription"
    )

    price = models.FloatField(
        default=00.00,
    )

    product_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    price_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    subscription_type = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        choices=SUBSCRIPTION_TYPE
    )
    description = models.TextField(null=True, blank=True)

    limit = models.PositiveIntegerField(default=20, null=True, blank=True)

    date_create = models.DateTimeField(
        verbose_name="Creation Date and Time",
        auto_now_add=True,
        help_text="Creation Date and Time",
    )

    last_update = models.DateTimeField(
        verbose_name="Last Update of Date and Time",
        auto_now=True,
        help_text="Last Update of Date and Time",
    )

    objects = SubscriptionManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_free:
            limit = self.limit
            if limit == 0:
                raise ValueError("Free Subscription should also have a limit")

            if limit is None:
                raise ValueError("Please provide limit for free Subscription")

            if self.price > float(0):
                raise ValueError("Free Subscription cannot have price greater than 0")

        return super().save(*args, **kwargs)

    @property
    def is_free(self):
        return self.price == float(0)

    @property
    def is_unlimited(self):
        return self.limit == None

    @property
    def is_weekly(self):
        return self.subscription_type == "wk"

    @property
    def is_monthly(self):
        return self.subscription_type == "mn"

    @property
    def is_yearly(self):
        return self.subscription_type == "yr"

    def get_next_subscription_date(self):
        time_del = self.SUBSCRIPTION_DAYS[self.subscription_type]
        return self.date_create + time_del

    def get_timedelta_in_days(self):
        time_del = self.SUBSCRIPTION_DAYS[self.subscription_type]
        now = timezone.now()
        return ((now + time_del) - now).days


@receiver(signal=post_save, sender=User)
def add_a_free_tier_when_user_created(sender, instance, created, **kwargs):
    if created:
        obj = Subscription.objects.get_default_free_subscription()
        if obj is None:
            return None
        
        obj.user.add(instance)
        obj.save()


class UserSubscription(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE
    )

    subscription = models.ForeignKey(
        to=Subscription,
        on_delete=models.CASCADE,
    )

    date_create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} > {self.subscription}"

    def has_expired(self):
        subscription = self.subscription
        user = self.user
        if float(subscription.price) == float(0):
            count = Message.objects.filter(room_id__create_user=user).count()
            return count > subscription.limit

        valid_till_date = subscription.get_next_subscription_date()
        now = timezone.now()
        return (now > valid_till_date)

