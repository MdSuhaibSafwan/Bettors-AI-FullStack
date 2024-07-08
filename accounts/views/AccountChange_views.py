from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, DeleteView
from common.lib.axes.utils import reset
from common.scripts import grecaptcha_request, RequestUtil
from ..forms import (
    OverlapPasswordChangeForm,
    OverlapSetPasswordForm,
    OverlapPasswordResetForm,
    EmailChangeForm,
    UserDeleteForm,
)
from ..models import ActivateToken
from ..views.send_mail.send_mail import send_token_for_change_email


User = get_user_model()


# Password Change
class OverlapPasswordChangeView(PasswordChangeView):
    template_name = "accounts/PasswordChange/password_change.html"
    form_class = OverlapPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "IS_USE_SIDENAV": True,
            }
        )
        return context


class OverlapPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/PasswordChange/password_change_done.html"
    success_url = reverse_lazy("accounts:password_reset_done")

    # 想定ルート(crrect_ref)から以外のアクセスを遮断
    def get(self, request, *args, **kwargs):
        siteurl = request._current_scheme_host
        crrect_ref = reverse("accounts:password_change")
        referer = RequestUtil.get_request_host_url(self)
        if not siteurl + crrect_ref == referer:
            reverse_url = reverse_lazy("home")
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "IS_USE_SIDENAV": True,
            }
        )
        return context


# Password Reset
# Referrer
# https://stackoverflow.com/questions/56015855/how-to-perform-additional-actions-on-passwordreset-in-django
# https://www.reddit.com/r/django/comments/q1ao3l/here_is_how_you_add_google_recaptcha_to_password/
class OverlapPasswordResetView(PasswordResetView):
    form_class = OverlapPasswordResetForm
    from_email = settings.DEFAULT_REPLY_EMAIL
    subject_template_name = "accounts/PasswordReset/mail_template/subject.html"
    email_template_name = "accounts/PasswordReset/mail_template/text_message.html"
    html_email_template_name = "accounts/PasswordReset/mail_template/html_message.html"
    extra_email_context = {"TOKEN_EXPIRED": int(settings.PASSWORD_RESET_TIMEOUT / 60)}
    success_url = reverse_lazy("accounts:password_reset_done")

    if settings.IS_USE_EMAIL_CERTIFICATION:
        template_name = "accounts/PasswordReset/password_reset.html"
    else:
        # If email certification is not used, password reset will be done by the administrator.
        template_name = "accounts/PasswordReset/password_reset_.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY
                if settings.IS_USE_RECAPTCHA
                else None,
                "IS_USE_RECAPTCHA": settings.IS_USE_RECAPTCHA,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Social login validation▽
        email = form["email"].value()
        user_or_none = User.objects.filter(email=email).first()
        try:
            is_set_password = user_or_none.is_set_password
        except:
            # Skip the check if the user is null to avoid revealing its non-existence (no email will be sent).
            is_set_password = True
        if not is_set_password:
            messages.add_message(
                self.request,
                messages.WARNING,
                "For social logins, please reset your password from the service you used.",
            )
            reverse_url = reverse_lazy("accounts:password_reset")
            return HttpResponseRedirect(reverse_url)
        # Social login validation△
        # reCaptcha token validation▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get("g-recaptcha-response")
            if recaptcha_token is None or recaptcha_token == "":
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    "Invalid POST request - reCaptcha ERROR",
                )
                reverse_url = reverse_lazy("accounts:password_reset")
                return HttpResponseRedirect(reverse_url)
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    if form.is_valid():
                        return self.form_valid(form)
                    else:
                        return self.form_invalid(form)
                else:  # reCaptcha FALSE
                    messages.add_message(
                        self.request,
                        messages.WARNING,
                        "Invalid POST request - reCaptcha ERROR",
                    )
                    reverse_url = reverse_lazy("accounts:password_reset")
                    return HttpResponseRedirect(reverse_url)
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        # reCaptcha token validation△

    def get_success_url(self):
        return self.success_url


class OverlapPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/PasswordReset/password_reset_done.html"

    # Prevent access from routes other than the expected route (correct_ref)
    def get(self, request, *args, **kwargs):
        site_url = request._current_scheme_host
        correct_ref = reverse("accounts:password_reset")
        referer = RequestUtil.get_request_host_url(self)
        if not site_url + correct_ref == referer:
            reverse_url = reverse_lazy("home")
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)


class OverlapPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/PasswordReset/password_reset_confirm.html"
    form_class = OverlapSetPasswordForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        reset(username=user.email)  # Reset django-axes for password reset
        messages.add_message(
            self.request,
            messages.INFO,
            "Your password has been changed. Please log in again with your new password.",
        )
        return super().form_valid(form)


# Email Address Change
class EmailChangeView(LoginRequiredMixin, FormView):
    model = User
    template_name = "accounts/EmailChange/email_change.html"
    form_class = EmailChangeForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY
                if settings.IS_USE_RECAPTCHA
                else None,
                "IS_USE_RECAPTCHA": settings.IS_USE_RECAPTCHA,
                "IS_USE_SIDENAV": True,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        # reCaptcha token validation▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get("g-recaptcha-response")
            if recaptcha_token is None or recaptcha_token == "":
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    "Invalid POST request - reCaptcha ERROR",
                )
                reverse_url = reverse_lazy("accounts:email_change")
                return HttpResponseRedirect(reverse_url)
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    pass
                else:  # reCaptcha FALSE
                    messages.add_message(
                        self.request,
                        messages.WARNING,
                        "Invalid POST request - reCaptcha ERROR",
                    )
                    reverse_url = reverse_lazy("accounts:email_change")
                    return HttpResponseRedirect(reverse_url)
        # reCaptcha token validation△
        user = self.request.user
        change_email = self.request.POST["change_email"]
        if user.is_set_password:
            if User.objects.filter(email=change_email).exists():
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    "This email address is already registered.",
                )
                reverse_url = reverse_lazy("accounts:email_change")
                return HttpResponseRedirect(reverse_url)
            else:  # SUCCESS
                return super().post(request, *args, **kwargs)
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                "To change the email address for users created with a social ID, please set a password first.",
            )
            reverse_url = reverse_lazy("accounts:password_change")
            return HttpResponseRedirect(reverse_url)

    def form_valid(self, form):
        user = self.request.user
        change_email = self.request.POST["change_email"]
        # Depending on whether email certification is used or not
        if settings.IS_USE_EMAIL_CERTIFICATION:
            user.is_change_email_request = True
            user.change_email = change_email
            user.save()
            send_token_for_change_email(user)
        else:
            user.is_change_email_request = False
            user.email = change_email  # Change the email address
            user.change_email = "dummy@mail.com"  # Set dummy data
            user.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Branching for post-signup page navigation depending on whether email certification is used or not
        if settings.IS_USE_EMAIL_CERTIFICATION:
            success_url = reverse_lazy("accounts:email_change_tmp_recept")
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                "Email address change completed.",
            )
            success_url = reverse_lazy("accounts:email_change")
        return success_url


class EmailChangeTmpReceptView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/EmailChange/email_change_tmp_recept.html"

    # Block access from users who haven't requested an email address change
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_change_email_request:
            reverse_url = reverse_lazy("home")
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "IS_USE_SIDENAV": True,
            }
        )
        return context


def ActivateEmailView(request, token):
    res, msg = ActivateToken.objects.activate_change_email_by_token(token)
    if res:
        logout(request)
        messages.add_message(request, messages.INFO, msg)
        reverse_url = reverse_lazy("accounts:login")
    else:
        messages.add_message(request, messages.WARNING, msg)
        reverse_url = reverse_lazy("home")
    return HttpResponseRedirect(reverse_url)


# Account Deletion
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/AccountDelete/delete.html"
    form_class = UserDeleteForm
    success_url = reverse_lazy("accounts:login")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(
            {
                "IS_USE_SIDENAV": True,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        check_text = self.request.POST["check_text"]

        if check_text == "delete":
            return super().post(request, *args, **kwargs)
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                "Check text error",
            )
            reverse_url = reverse_lazy("accounts:delete")
            return HttpResponseRedirect(reverse_url)

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(
            self.request,
            messages.INFO,
            "Your account has been deleted. Thank you for using our services.",
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url
