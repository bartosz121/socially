from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from posts.models import Post
from pathlib import Path
import uuid

from .mixins import ResizeImageMixin


User = settings.AUTH_USER_MODEL


def profile_images_handler(instance, filename):
    fpath = Path(filename)
    new_filename = f"{str(uuid.uuid4())}{fpath.suffix}"
    return f"profile_images/{new_filename}"


class Profile(
    models.Model,
    ResizeImageMixin,
):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    username = models.CharField(
        "username",
        max_length=40,
        unique=True,
        default=None,
        help_text="Required. 40 characters or fewer.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    profile_picture = models.ImageField(
        upload_to=profile_images_handler,
        default="profile_images/profile_default.png",
    )
    profile_background = models.ImageField(
        upload_to=profile_images_handler,
        default="profile_images/background_default.jpg",
    )
    bio = models.TextField(
        max_length=180, help_text="Write something about yourself!", blank=True
    )
    followers = models.ManyToManyField(
        "Profile", related_name="following", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.user.pk} - {self.username}"

    def get_posts_count(self):
        return self.posts.all().count()

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()

    def save(self, *args, **kwargs):
        self.resize(self.profile_picture.path, settings.PROFILE_PICTURE_SIZE)
        self.resize(
            self.profile_background.path, settings.PROFILE_BACKGROUND_SIZE
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "profiles:profile-detail", kwargs={"username": self.username}
        )


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        username = instance.email.split("@")[0]
        Profile.objects.get_or_create(user=instance, username=username)


post_save.connect(user_did_save, sender=User)
