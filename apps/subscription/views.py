from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subscription


@login_required
def subscription_list_view(request):
	subscriptions = Subscription.objects.all().order_by("-last_update")

	context = {
		"subscriptions": subscriptions,
	}
	
	return render(request, "apps/subscription/subscription_list.html", context)
