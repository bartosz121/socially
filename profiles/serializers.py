from django.conf import settings
from django.forms import ValidationError
from rest_framework import serializers

from mixins.compare_images_mixin import CompareImagesMixin

from .models import Profile
from .signals import post_save_check_images


class ProfileBasicSerializer(serializers.ModelSerializer):
    """
    Basic profile information
    """

    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    username = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user_id",
            "username",
            "profile_picture",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user_id",
            "username",
            "profile_picture",
            "profile_background",
            "bio",
            "followers_count",
            "following_count",
            "posts_count",
            "created",
            "updated",
        ]

    def get_followers_count(self, obj):
        return obj.get_followers_count()

    def get_following_count(self, obj):
        return obj.get_following_count()

    def get_posts_count(self, obj):
        return obj.user.get_posts_count()


class ProfileFollowSerializer(serializers.Serializer):
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower()
        if value not in ("follow", "unfollow"):
            raise serializers.ValidationError(f"Action {value!r} is not valid")

        return value


class ProfileFollowCountSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user_id",
            "username",
            "followers",
            "following",
        ]

    def get_followers(self, obj):
        return obj.get_followers_count()

    def get_following(self, obj):
        return obj.get_following_count()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username", "profile_picture", "profile_background", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_profile_picture_to_default(self, profile):
        profile.profile_picture = Profile.profile_picture.field.default

    def _set_profile_background_to_default(self, profile):
        profile.profile_background = Profile.profile_background.field.default

    def update(self, instance, validated_data):
        old_images = {
            "profile_picture": instance.profile_picture.path,
            "profile_background": instance.profile_background.path,
        }

        if not validated_data.get("profile_picture", None):
            self._set_profile_picture_to_default(instance)

        if not validated_data.get("profile_background", None):
            self._set_profile_background_to_default(instance)

        updated_instance = super().update(instance, validated_data)

        post_save_check_images.send(
            sender=Profile,
            instance=instance,
            created=False,
            old_images=old_images,
        )

        return updated_instance
