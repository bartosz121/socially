from django.db import models
from django.conf import settings

# Create your models here.


class Post(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    picture = models.ImageField(upload_to="pictures", blank=True)
    body = models.TextField(max_length=300)
    author = models.ForeignKey(
        "profiles.Profile",
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

    def get_liked(self):
        """Return users that liked the post"""
        return self.liked.all()

    def get_user_liked(self, user):
        """Did given user like the post"""
        return user in self.get_liked()

    @property
    def like_count(self):
        return self.liked.all().count()

    @property
    def author_username(self):
        return self.author.username
