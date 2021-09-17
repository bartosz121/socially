from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Profile


class RegistrationProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["username"]
        exclude = ["profile_picture", "profile_background", "bio"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "profile_picture", "profile_background", "bio"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            profile = Profile.objects.exclude(user=self.instance.user).get(
                username=username
            )
            raise ValidationError("This username is in use.")
        except Profile.DoesNotExist:
            return username

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        profile.username = self.cleaned_data["username"]
        profile.profile_picture = self.cleaned_data["profile_picture"]
        profile.profile_background = self.cleaned_data["profile_background"]
        profile.bio = self.cleaned_data["bio"]
        if commit:
            profile.save()
        return profile
