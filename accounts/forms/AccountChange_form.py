from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordForm,
    PasswordResetForm,
    _unicode_ci_compare,
)

User = get_user_model()


# Password Change
class OverlapPasswordChangeForm(SetPasswordForm):
    field_order = ["new_password1", "new_password2"]

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.is_change_email_request = False  # Reset email change request
            self.user.is_set_password = (
                True  # Check if password is set (initially set to False for social IDs)
            )
            self.user.save()
        return self.user


# Password Reset
class OverlapSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.change_email_on_request = False  # Reset email change request
            self.user.save()
        return self.user


# Password Reset
class OverlapPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{
                "email": email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )


# Email Change
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "change_email",
        ]


# Account Deletion
class UserDeleteForm(forms.Form):
    check_text = forms.CharField(
        label="Confirmation",
        required=True,
        help_text='To delete, enter "delete" and press the button.',
    )
