import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from profiles.models import Profile


class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique indentifier
    instead of username
    """

    def create_user(self, email, password, superuser=False, **fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()
        if superuser:
            Profile(user=user, username=str(uuid.uuid4()).split("-")[0]).save()
        return user

    def create_superuser(self, email, password, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        fields.setdefault("is_active", True)

        if fields.get("is_staff") is not True:
            raise ValueError("Superuser must have 'is_staff' set to True")
        if fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have 'is_superuser' set to True")

        return self.create_user(email, password, superuser=True, **fields)


class CustomUser(AbstractUser):
    username = None  # username will be in 'Profile' model
    email = models.EmailField("Email address", unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"User #{self.pk} {self.email}"
