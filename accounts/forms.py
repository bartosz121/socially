from accounts.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class EmailAddressForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean(self):
        email = self.cleaned_data.get("email")

        if not CustomUser.objects.filter(email=email).exists():
            return {"email": email}
        raise forms.ValidationError(
            "User with this Email address already exists."
        )


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
