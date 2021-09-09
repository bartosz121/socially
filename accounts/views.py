from django.shortcuts import render, redirect
from django.views.generic import View
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
            return redirect("accounts:login")
    else:
        user_form = CustomUserCreationForm()
        profile_form = RegistrationProfileForm()
        print(user_form.fields)
        print(profile_form.fields)
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class SettingsView(View):
    template_name = "accounts/settings.html"

    def get_context_data(self, **kwargs):
        if "email_form" not in kwargs:
            kwargs["email_form"] = EmailAddressForm(
                initial={"email": self.request.user.email}
            )
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = ProfileForm(
                instance=self.request.user.profile
            )

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if "email_form" in request.POST:
            print(request.POST)
            email_form = EmailAddressForm(request.POST)

            if email_form.is_valid():
                email = email_form.cleaned_data.get("email")
                user = CustomUser.objects.get(pk=self.request.user.pk)
                user.email = email
                user.save()

            else:
                context["email_form"] = email_form
                print(email_form.cleaned_data)
        if "profile_form" in request.POST:
            print(request.FILES)
            profile_form = ProfileForm(
                request.POST, instance=self.request.user.profile
            )

            if profile_form.is_valid():
                profile_form.save()

            else:
                context["profile_form"] = profile_form

        return render(
            request, self.template_name, self.get_context_data(**context)
        )
