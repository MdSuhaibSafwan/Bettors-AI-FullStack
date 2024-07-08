from django.urls import path
from . import views

urlpatterns = [
	path("manage/", views.subscription_list_view, name="subscription-list"),
]
