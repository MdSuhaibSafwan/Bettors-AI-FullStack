from django.contrib import admin
from .models import StripeCustomer, StripeCheckout, StripePaymentLink

admin.site.register(StripeCustomer)
admin.site.register(StripeCheckout)
admin.site.register(StripePaymentLink)
