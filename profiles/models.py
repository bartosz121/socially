from django.db import models
from django.conf import settings
from django.urls import reverse
from posts.models import Post

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
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
        upload_to="profile_pictures", default="profile_pictures/default.png"
    )
    profile_background = models.ImageField(
        upload_to="profile_backgrounds",
        default="profile_backgrounds/default.png",
    )
    bio = models.TextField(
        max_length=180, help_text="Write something about yourself!", blank=True
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="following", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.user.pk} - {self.username}"

    @property
    def posts_count(self):
        return self.posts.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    @property
    def followers_count(self):
        return len(self.get_followers())

    def get_absolute_url(self):
        return reverse(
            "profiles:profile-detail", kwargs={"username": self.username}
        )

    def get_posts(self):
        return self.posts.all().order_by("-created")

    def get_following_profiles(self):
        return list(
            Profile.objects.get(user=user) for user in self.following.all()
        )

    def get_user_follow_status(self, target_user):
        """Is 'this' user following given user"""
        return target_user.profile in self.get_following_profiles()

    def get_following_users_posts(self):
        # for user in self.get_following_profiles():
        #     posts.append(Post.objects.filter(author=user))
        # if len(posts) > 0:
        #     return sorted(
        #         chain(*posts), reverse=True, key=lambda post: post.created
        #     )
        posts = (
            Post.objects.all()
            .filter(author__in=self.get_following_profiles())
            .order_by("-created")
        )
        return posts

    def get_followers(self):
        qs = Profile.objects.all().exclude(user=self.user)
        followers = [
            profile
            for profile in qs
            if self in profile.get_following_profiles()
        ]
        return followers

    # TODO make this more 'smart'
    def get_follow_suggestions(self):
        profiles = Profile.objects.all().exclude(user=self.user)
        following = [profile for profile in self.get_following_profiles()]
        profiles = list(
            filter(lambda profile: profile not in following, profiles)
        )
        if len(profiles) > 3:
            return profiles[:3]
        return profiles
