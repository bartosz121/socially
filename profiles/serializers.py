from rest_framework import serializers

from .models import Profile


class ProfilePostInlineSerializer(serializers.Serializer):
    """
    Provides basic profile information
    """

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(read_only=True)
    profile_url = serializers.HyperlinkedIdentityField(
        view_name="profiles:profile-detail",
        lookup_field="username",
        read_only=True,
    )


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.pk", read_only=True)
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
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
            "follower_count",
            "following_count",
            "url",
            "created",
            "updated",
        ]

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
