from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.utils import get_paginated_queryset_response
from posts.models import Post
from posts.serializers import PostSerializer
from profiles.models import Profile


class UserViewSet(viewsets.GenericViewSet):
    # Profile queryset because we use username as identifier in urls
    queryset = Profile.objects.all()
    lookup_field = "profile__username"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=True, url_name="posts", url_path="posts")
    def user_posts(self, request, profile__username=None):
        qs = self.get_queryset()
        user: Profile = get_object_or_404(qs, username=profile__username)
        user_posts_qs = Post.objects.user_posts(user)

        return get_paginated_queryset_response(
            self.paginator, request, user_posts_qs, PostSerializer
        )

    @action(
        methods=["GET"],
        detail=True,
        url_name="feed",
        url_path="feed",
    )
    def user_feed(self, request, profile__username=None):
        qs = self.get_queryset()
        user: Profile = get_object_or_404(qs, username=profile__username)

        feed_qs = Post.objects.user_feed(user)

        return get_paginated_queryset_response(
            self.paginator, request, feed_qs, PostSerializer
        )

    @action(
        methods=["GET"],
        detail=True,
        url_name="liked",
        url_path="liked/(?P<post_pk>[0-9]+)",
    )
    def user_liked(self, request, profile__username=None, post_pk=None):
        user_qs = self.get_queryset()
        user = get_object_or_404(user_qs, username=profile__username)

        post_qs = Post.objects.all()
        post = get_object_or_404(post_qs, pk=post_pk)

        is_liked = post.likes.filter(id=user.id).exists()

        return Response({"is_liked": is_liked})
