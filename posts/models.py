from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from pathlib import Path
import uuid

User = settings.AUTH_USER_MODEL


def post_image_upload_handler(instance, filename):
    fpath = Path(filename)
    new_filename = f"{str(uuid.uuid4())}{fpath.suffix}"
    return f"pictures/{new_filename}"


class PostQuerySet(models.QuerySet):
    def latest(self):
        return self.order_by("-created")

    def feed(self, user):
        """
        Returns posts created by followed user authors.
        If not following anyone return latest posts
        """
        profile = user.profile

        is_following_anyone = profile.following.exists()
        followed_users_id = []
        if not is_following_anyone:
            return self.latest()

        followed_users_id = profile.following.values_list("user_id", flat=True)

        return (
            self.filter(Q(author_id__in=followed_users_id) | Q(author=user))
            .distinct()
            .order_by("-created")
        )


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def latest(self):
        return self.get_queryset().latest()

    def user_feed(self, user):
        return self.get_queryset().feed(user)


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
        related_name="posts",
    )
    likes = models.ManyToManyField(
        User, blank=True, related_name="liked", through="PostLike"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def __str__(self):
        return f"{self.pk} by {self.author.profile.username}"

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})

    def get_comment_count(self):
        return Post.objects.filter(parent=self).count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
