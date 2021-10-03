import factory

from profiles.models import Profile
from accounts.tests.factories import CustomUserFactory, CustomSuperUserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(CustomUserFactory)
    username = factory.Faker("user_name")
    bio = factory.Faker("text", max_nb_chars=180)


class SuperUserProfileFactory(ProfileFactory):
    user = factory.SubFactory(CustomSuperUserFactory)
