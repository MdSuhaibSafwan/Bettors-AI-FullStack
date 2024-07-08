import json
import stripe
import urllib
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import StripeCheckout
from django.core.exceptions import ObjectDoesNotExist
from apps.subscription.models import Subscription
from .models import StripePaymentLink
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class StripeAdapter(object):

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

    def register_stripe_customer(self, user, customer_id, subscription_id, session_data=None):
        country = session_data.customer_details.address.country
        email = session_data.customer_details.email
        name = session_data.customer_details.name

        customer = user.stripecustomer_set.create(
            stripe_customer_id=customer_id,
            stripe_subscription_id=subscription_id,
            customer_email=email,
            customer_country=country,
            customer_name=name,
        )

        subscription_id = session_data.subscription
        payment_link = session_data.payment_link
        invoice_id = session_data.invoice
        transaction_id = session_data.id
        currency_used = session_data.currency
        raw_data = json.loads(json.dumps(session_data))

        StripeCheckout.objects.create(
            customer=customer,
            payment_link=payment_link,
            subscription_id=subscription_id,
            invoice_id=invoice_id,
            transaction_id=transaction_id,
            currency_used=currency_used
        )

        return customer

    def create_checkout_session(self, user):
        checkout_session = self.stripe.checkout.Session.create(
            client_reference_id=user.id,
            success_url=self.get_success_url(),
            cancel_url=self.get_failure_url(),
            payment_method_types=["card", ],
            mode="subscription",
            line_items=[
                {
                    "price": settings.STRIPE_SUBSCRIPTION_PRICE_ID,
                    "quantity": 1
                }
            ],
        )

        return checkout_session

    def get_publishable_key(self):
        return settings.STRIPE_PUBLISHABLE_KEY

    def handle_webhook_request(self, request):
        wh_secret = settings.STRIPE_WEBHOOK_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = self.stripe.Webhook.construct_event(
                payload, sig_header, wh_secret
            )
        except stripe.error.SignatureVerificationError as e:
            raise ValueError(e)


        if event['type'] == 'checkout.session.completed':
            return self.stripe_webhook_checkout_session_completed(request, event)

        if event['type'] == 'payment_link.created':
            return self.stripe_webhook_payment_link_created(request, event)

    def stripe_webhook_payment_link_created(self, request, event):
        session = event['data']['object']
        meta = session.get("metadata")
        user_id = meta.get("user_id", None)
        if user_id is None:
            raise ValueError("No user id found")
                  
        payment_link = session.get("url", None)
        if not payment_link:
            raise ValueError("URL not found for payment link")
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        return self.add_payment_link_to_db(user, payment_link)

    def add_payment_link_to_db(self, user, link):
        return StripePaymentLink.objects.create(
            user=user,
            payment_link=link,
        )

    def stripe_webhook_checkout_session_completed(self, request, event):
        session = event['data']['object']
        meta = session.get("metadata")
        user_id = meta.get("user_id", None)
        subscription_id = meta.get("subscription_id", None)
        if user_id is None:
            raise ValueError("No user id found")
            
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new Stripe Customer
        user = User.objects.get(id=user_id)
        self.add_subscription_to_user(user, subscription_id)
        return self.register_stripe_customer(
            user, stripe_customer_id, stripe_subscription_id, session
        )

    def remove_previous_user_subscriptions(self, user):
        previous_subs_qs = Subscription.objects.filter(user=user)
        for obj in previous_subs_qs:
            obj.user.remove(user)
            obj.save()

        return previous_subs_qs

    def add_subscription_to_user(self, user, subscription_id):
        self.remove_previous_user_subscriptions(user)
        try:
            obj = Subscription.objects.get(id=subscription_id)
        except ObjectDoesNotExist as e:
            raise ValueError(e)

        obj.user.add(user)
        obj.save()
        return obj

    def get_success_url(self):
        domain = "http://127.0.0.1:8000"
        return domain + reverse("subscription-list")

    def get_failure_url(self):
        domain = "http://127.0.0.1:8000"
        return domain + reverse("subscription-list")

    def create_text_for_payment_link_of_all_subscriptions(self, user):
        subscription_qs = Subscription.objects.get_paid_subscriptions()
        starting_txt = self.create_text_for_payment_link()
        for subscription in subscription_qs:
            starting_txt += f"""
                Package Name: {subscription.name},
                Price: {subscription.price},
                Click on the link to pay {self.create_payment_link(user, subscription.id)}
            """

        return starting_txt


    def create_payment_link(self, user, subscription_id):
        is_elegible = user.is_eligible_for_next_subscription()
        if not is_elegible:
            raise ValueError("User Already have a subscription")

        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except ObjectDoesNotExist as e:
            raise ValueError(e)

        price = subscription.price_id
        try:
            now = timezone.now()
            trial_period_days = subscription.get_timedelta_in_days()
            next_date_in_str = (now+timedelta(days=trial_period_days)).strftime('%m/%d/%Y')
            metadata = {
                "user_id": user.id,
                "subscription_id": subscription.id
            }
            payment_link = self.stripe.PaymentLink.create(
                line_items=[
                    {"price": price, "quantity": 1}
                ],
                metadata=metadata,
                currency="usd",
                after_completion={
                    "redirect": {
                        "url": self.get_success_url(),
                    },
                    "type": "redirect",
                },
                subscription_data={
                    "description": getattr(subscription, "description", f"Subscription until {next_date_in_str}"),
                    "invoice_settings": {
                        "issuer": {
                            "type": "self",
                        }
                    },
                    "metadata": metadata,
                    "trial_period_days": trial_period_days,
                    "trial_settings": {
                        "end_behavior": {
                            "missing_payment_method": "pause" #Pause the subscription when the trial ends.
                        }
                    }
                },
                # Add Display Information
            )

        except stripe._error.InvalidRequestError as e:
            raise ValueError(e)

        url = payment_link.url
        parameters = urllib.parse.urlencode({"prefilled_email": user.email})
        url = f"{url}?{parameters}"
        return url

    def create_text_for_payment_link(self, link=""):
        a = f"""
            It seems that you have reached the end of your trial. You can continue using our service by subscribing to our 
            unlimited plan. I have generate a link for you so you can easily subscribe! {link}.
        """
        return a
