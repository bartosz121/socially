from rest_framework import serializers

from .models import Profile


class ProfileBasicSerializer(serializers.ModelSerializer):
    """
    Basic profile information
    """

    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    username = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = ["user_id", "username", "profile_picture",]


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="profiles:profile-detail",
        lookup_field="username",
        read_only=True,
    )

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
            "url",
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
