from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", default="profile_pictures/default.png"
    )
    profile_background = models.ImageField(
        upload_to="profile_backgrounds",
        default="profile_backgrounds/default.png",
    )
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(
        User, related_name="following", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.user.pk} - {self.user.username}"

    def get_posts(self):
        return self.posts.all()

    @property
    def posts_count(self):
        return self.posts.all().count()
