from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile

# Create your models here.


class Post(models.Model):
    picture = models.ImageField(upload_to="pictures", blank=True)
    body = models.TextField(max_length=300)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None, related_name="posts"
    )
    liked = models.ManyToManyField(User, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} by {self.author.user.username}"

    def get_liked(self):
        """Returns users that liked the post"""
        return self.liked.all()

    def get_user_liked(self, user):
        """Does given user liked the post"""
        pass

    @property
    def like_count(self):
        return self.liked.all().count()
