from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import *
from apps.chat.models import Message

User = get_user_model()


class StripePaymentLink(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="Payment Link of a User",
    )
    payment_link = models.URLField()

    date_create = models.DateTimeField(
        verbose_name="Creation Date and Time",
        auto_now_add=True,
        help_text="Creation Date and Time",
    )

    def __str__(self):
        return self.payment_link


class StripeCustomer(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="User for Stripe Checkout",
    )

    stripe_customer_id = models.CharField(
        max_length=300,
        help_text="Customer Id of a Stripe user"
    )

    stripe_subscription_id = models.CharField(
        max_length=300,
        help_text="Subscription id of user",
        null=True
    )

    customer_email = models.EmailField(null=True)
    customer_country = models.CharField(
        max_length=1000, null=True
    )
    customer_name = models.CharField(
        max_length=100, null=True
    )

    date_create = models.DateTimeField(
        verbose_name="Creation Date and Time",
        auto_now_add=True,
        help_text="Creation Date and Time",
    )

    def __str__(self):
        return f"<Stripe {self.user}>"



class StripeCheckout(models.Model):
    customer = models.OneToOneField(
        StripeCustomer,
        on_delete=models.CASCADE,
    )
    payment_link = models.CharField(
        max_length=100,
    )
    subscription_id = models.CharField(
        max_length=100,
    )
    currency_used = models.CharField(
        max_length=3,
    )
    transaction_id = models.CharField(
        max_length=264,
    )
    invoice_id = models.CharField(
        max_length=264,
    )
    raw_data = models.JSONField(
        default=dict
    )

    def __str__(self):
        return str(self.invoice_id)
