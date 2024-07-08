from django import forms
from .models import UserProfile
from apps.subscription.models import Subscription


class UserProfileAdminForm(forms.ModelForm):
	subscription = forms.CharField(
	    max_length=100,
	    widget=forms.TextInput(attrs={'disabled': True, 'required': False}),

	)

	class Meta:
		model = UserProfile
		fields = "__all__"
		read_only_fields = ["subscription", ]
