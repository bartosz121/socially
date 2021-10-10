from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import DeleteView
from profiles.forms import RegistrationProfileForm, ProfileForm
from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    EmailAddressForm,
)

# Create your views here.


def register(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = RegistrationProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            created_user = user_form.save()
            profile_form.instance.user = created_user
            profile_form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect("accounts:login")

        else:
            messages.error(request, "Please correct the error below.")
            user_form = CustomUserCreationForm(request.POST)
            profile_form = RegistrationProfileForm(request.POST)
    else:
        if request.user.is_authenticated:
            return redirect("posts:home-view")
        user_form = CustomUserCreationForm()
        profile_form = RegistrationProfileForm()

    return render(
        request,
        "accounts/registration/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class SettingsView(View):
    template_name = "accounts/settings.html"

    def get_context_data(self, **kwargs):
        if "email_form" not in kwargs:
            kwargs["email_form"] = EmailAddressForm(
                initial={"email": self.request.user.email},
                user_obj=self.request.user,
            )
        if "password_change_form" not in kwargs:
            kwargs["password_change_form"] = PasswordChangeForm(
                self.request.user
            )
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = ProfileForm(
                instance=self.request.user.profile
            )

        return kwargs

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if "email_form" in request.POST:
            email_form = EmailAddressForm(
                user_obj=request.user, data=request.POST
            )

            if email_form.is_valid():
                email = email_form.cleaned_data.get("email")
                user = CustomUser.objects.get(pk=request.user.pk)
                user.email = email
                user.save()
                messages.success(request, "Email address changed.")
                return redirect("accounts:settings")

            else:
                messages.error(request, "Please correct the error below.")
                context["email_form"] = email_form

        if "password_change_form" in request.POST:
            password_change_form = PasswordChangeForm(
                request.user, request.POST
            )

            if password_change_form.is_valid():
                password_change_form.save()
                update_session_auth_hash(request, password_change_form.user)
                messages.success(request, "Password changed.")
                return redirect("accounts:settings")
            else:
                messages.error(request, "Please correct the error below.")
                context["password_change_form"] = password_change_form

        if "profile_form" in request.POST:
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=request.user.profile
            )

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect("accounts:settings")

            else:
                messages.error(request, "Please correct the error below.")
                context["profile_form"] = profile_form

        return render(
            request, self.template_name, self.get_context_data(**context)
        )


class DeleteUser(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy("posts:home-view")
    success_message = "Account deleted"
    template_name = "accounts/confirm_delete.html"

    def test_func(self):
        user_obj = self.get_object()
        return user_obj == self.request.user
