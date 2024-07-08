from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


# ログイン
class LogInForm(AuthenticationForm):

    is_login_remenber = forms.BooleanField(
                            label    = 'Stay logged in.',
                            required = False)