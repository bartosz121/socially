from django.db import models
from django.urls import reverse
from django.conf import settings
from pathlib import Path
import uuid

User = settings.AUTH_USER_MODEL


def post_image_upload_handler(instance, filename):
    fpath = Path(filename)
    new_filename = f"{str(uuid.uuid4())}{fpath.suffix}"
    return f"pictures/{new_filename}"


class Post(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    picture = models.ImageField(
        upload_to=post_image_upload_handler, blank=True
    )
    body = models.TextField(max_length=settings.MAX_POST_LENGTH)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name="posts",
    )
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        default=None,
        blank=True,
        related_name="liked",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} by {self.author.username}"

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})

    def get_liked(self):
        """Return users that liked the post"""
        return self.liked.all()

    def get_comments(self):
        """Return posts with 'parent' set to 'this' post"""
        return Post.objects.filter(parent=self).order_by("-updated")

    def get_user_liked(self, user):
        """Did given user like the post"""
        return user in self.get_liked()

    @property
    def like_count(self):
        return self.liked.all().count()

    @property
    def comment_count(self):
        return self.get_comments().count()

    @property
    def author_username(self):
        return self.author.username
