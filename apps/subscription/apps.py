from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscription'

    def ready(self):
        super().ready()
        try:
            from .models import Subscription
            qs = Subscription.objects.get_free_subscriptions()
            if not qs.exists():
                subscription = Subscription(
                    name="free-tier",
                    price=0,
                    limit=20,
                )
                subscription.save()
        except Exception as e:
            print(e)
