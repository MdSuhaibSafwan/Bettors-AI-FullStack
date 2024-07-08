from django.shortcuts import render
from .adapters import StripeAdapter
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import StripeCustomer
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class CSRFExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class StripeWebhookView(CSRFExemptMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        stripe_adapter = StripeAdapter()
        try:
            stripe_adapter.handle_webhook_request(request)
        except ValueError as e:
            return JsonResponse({"success": False, "error_data": e}, safe=False)

        return JsonResponse({"success": True}, safe=False)

    def get(self, request, *args, **kwargs):
        pass


class CreateProductPaymentLink(LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        subscription_id = request.POST.get("subscription-id", None)
        if subscription_id is None:
            data = {
                "status_code": 400,
                "message": "No Subscription Id found",
            }
            return JsonResponse(data, safe=False)

        try:
            stripe_adapter = StripeAdapter()
            payment_link = stripe_adapter.create_payment_link(request.user, subscription_id)

            data = {
                "success": True,
                "status_code": 200,
                "payment_link_url": payment_link
            }
        except ValueError as e:
            data = {
                "status_code": 400,
                "message": str(e),
            }
        return JsonResponse(data, safe=False)


def payment_success_page(request):
    return render(request, "apps/payment/payment_success.html", )


def payment_error_page(request):
    return render(request, "apps/payment/payment_error.html", )
