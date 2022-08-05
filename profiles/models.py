import os
from typing import Dict
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.db.models import Count
from pathlib import Path
import uuid
from mixins.compare_images_mixin import CompareImagesMixin

from mixins.remove_file_mixin import RemoveFileMixin
from mixins.resize_image_mixin import ResizeImageMixin

from .signals import post_save_check_images


User = settings.AUTH_USER_MODEL


def profile_images_handler(instance, filename):
    fpath = Path(filename)
    new_filename = f"{str(uuid.uuid4())}{fpath.suffix}"
    return f"profile_images/{new_filename}"


class ProfileQuerySet(models.QuerySet):
    def with_followers_count(self):
        """Annotate queryset with `followers_count`"""
        return self.annotate(followers_count=Count("followers"))

    def get_follow_suggestions(self, profile_to_suggest):
        return self.with_followers_count().exclude(
            id__in=profile_to_suggest.following.values("id")
        )


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, self._db).order_by("-created")

    def most_followers(self, *, n=5):
        queryset = self.get_queryset().with_followers_count()
        return queryset.order_by("-followers_count")[:n]

    def follow_suggestions(self, profile, *, n=5):
        queryset = (
            self.get_queryset()
            .get_follow_suggestions(profile)
            .order_by("-followers_count")
        )
        return queryset[:n]


class Profile(models.Model):
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

    objects = ProfileManager()

    # TODO properties will be removed after HTMX would be dropped
    @property
    def followers_counter(self):
        return self.followers.count()

    def __str__(self):
        return f"#{self.pk} - {self.username}"

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()

    def is_using_default_profile_picture(self) -> bool:
        return (
            os.path.split(self.profile_picture.path)[-1]
            == os.path.split(self.profile_picture.field.default)[-1]
        )

    def if_using_default_background_picture(self) -> bool:
        return (
            os.path.split(self.profile_background.path)[-1]
            == os.path.split(self.profile_background.field.default)[-1]
        )

    def get_absolute_url(self):
        return reverse(
            "profiles:profile-detail", kwargs={"username": self.username}
        )


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        username = instance.email.split("@")[0]
        Profile.objects.get_or_create(
            user=instance, pk=instance.pk, username=username
        )


def profile_check_images_post_save(
    sender, instance, created, old_images: Dict[str, str], *args, **kwargs
):
    """Checks if new image is the same as old one, if yes use old one and remove new and resize"""
    resizer = ResizeImageMixin()
    remover = RemoveFileMixin()
    comparer = CompareImagesMixin()

    for key, path in old_images.items():
        current = getattr(instance, key)
        _, filename = os.path.split(path)
        if comparer.imgs_are_equal(current.path, path):
            setattr(instance, key, f"profile_images/{filename}")
            # set filename and path to new image, it will be deleted
            _, filename = os.path.split(current.path)
            path = current.path

        if filename not in (
            "profile_default.png",
            "background_default.jpg",
        ):
            remover.remove_file(path)

    instance.save()

    resizer.resize(instance.profile_picture.path, settings.PROFILE_PICTURE_SIZE)
    resizer.resize(
        instance.profile_background.path, settings.PROFILE_BACKGROUND_SIZE
    )




post_save.connect(user_did_save, sender=User)
post_save_check_images.connect(profile_check_images_post_save, sender=Profile)
