from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Post
from profiles.serializers import ProfileBasicSerializer

User = settings.AUTH_USER_MODEL


class PostParentSerializer(serializers.ModelSerializer):
    parent_author = ProfileBasicSerializer(
        source="author.profile", read_only=True
    )
    parent_url = serializers.HyperlinkedIdentityField(
        source="url",
        view_name="posts:post-detail",
        lookup_field="pk",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "parent_author",
            "parent_url",
        ]


class PostSerializer(serializers.ModelSerializer):
    parent_post = PostParentSerializer(source="parent", read_only=True)
    post_author = ProfileBasicSerializer(
        source="author.profile", read_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="posts:post-detail",
        lookup_field="pk",
        read_only=True,
    )
    picture_url = serializers.ImageField(
        source="picture", allow_empty_file=True, required=False
    )
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "parent_post",
            "body",
            "picture_url",
            "like_count",
            "comment_count",
            "url",
            "edit_url",
            "post_author",
            "created",
            "updated",
        ]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()

    def get_edit_url(self, obj):
        request = self.context.get("request")
        return reverse(
            "posts:post-update", kwargs={"pk": obj.pk}, request=request
        )


class PostLikeSerializer(serializers.Serializer):
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower()
        if value not in ("like", "dislike"):
            raise serializers.ValidationError(f"Action {value!r} is not valid")

        return value
