from django.urls import path
from . import views

urlpatterns = [
    path("success/", views.payment_success_page, name="payment-success-page"),
    path("create-payment-link/", views.CreateProductPaymentLink.as_view(), name="create-payment-link"),
    path("failure/", views.payment_error_page, name="payment-failure-page"),
    path("webhook/", views.StripeWebhookView.as_view(), name="stripe-webhook"),
]
