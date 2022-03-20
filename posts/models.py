from django.db import models
from django.db.models import Q, Count, OuterRef, Subquery
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

    def comments_to(self, post):
        return self.filter(parent=post).order_by("-created")

    def by_user(self, user):
        return self.filter(author=user).order_by("-created")

    def with_comment_count(self):
        """Annotate queryset with `comments_count`"""
        subquery_parent_count = Post.objects.filter(parent_id=OuterRef("pk"))
        return self.annotate(
            comments_count=Count(
                Subquery(subquery_parent_count.values("pk")[:1])
            )
        )


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def latest(self):
        return self.get_queryset().latest()

    def user_feed(self, user):
        return self.get_queryset().feed(user)

    def get_comments(self, post):
        return self.get_queryset().comments_to(post)

    def most_comments(self, *, n=5):
        queryset = self.get_queryset().with_comment_count()
        return queryset.order_by("-comments_count")[:n]

    def user_posts(self, user):
        return self.get_queryset().by_user(user)


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

    # TODO properties will be removed after HTMX will be dropped
    @property
    def comment_count(self):
        return Post.objects.filter(parent=self).count()

    @property
    def like_count(self):
        return self.likes.count()

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
