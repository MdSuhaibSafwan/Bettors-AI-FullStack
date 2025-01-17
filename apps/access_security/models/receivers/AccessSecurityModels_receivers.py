from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from ...models import AccessSecurity


@receiver(post_save, sender=AccessSecurity)
def access_security_notice_admin(sender, instance, **kwargs) -> None:
    if kwargs["created"]:
        if settings.IS_NOTIFICATION_ADMIN:
            if instance.type == "SET_BLOCK_IP":
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = settings.ADMIN_NOTICE_EMAIL
                subject = "AccessSecurity Alert!"
                body = f"{instance.ip} has been added to the blocklist due to excessive access"
                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=body,
                    from_email=from_email,
                    to=[to_email],
                )
                email_message.send(fail_silently=False)
