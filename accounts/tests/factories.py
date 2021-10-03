import factory
from accounts.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker("email")
    password = "Password123!@#"
    is_active = True
    is_staff = False
    is_superuser = False


class CustomSuperUserFactory(CustomUserFactory):
    is_staff = True
    is_superuser = True
