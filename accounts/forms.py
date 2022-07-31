from accounts.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class ChangeEmailAddressForm(forms.Form):
    new_email1 = forms.EmailField(label="Email address", required=True)
    new_email2 = forms.EmailField(label="Confirm email address", required=True)

    def __init__(self, user, *args, **kwargs):
        super(ChangeEmailAddressForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_new_email1(self):
        new_email = self.cleaned_data.get("new_email1")

        if (
            not CustomUser.objects.exclude(pk=self.user.pk)
            .filter(email=new_email)
            .exists()
        ):
            return new_email
        raise forms.ValidationError(
            "User with this Email address already exists."
        )

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get("new_email1")
        new_email2 = self.cleaned_data.get("new_email2")
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    "New emails dont match", code="new_email_mismatch"
                )
        return new_email2

    def save(self, commit=True):
        new_email = self.cleaned_data["new_email1"]
        self.user.email = new_email
        if commit:
            self.user.save()
        return self.user


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = False
