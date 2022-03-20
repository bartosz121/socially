from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsUserOrIsStaff
from api.utils import get_paginated_queryset_response
from posts.models import Post
from posts.serializers import PostSerializer
from .models import CustomUser


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=True, url_name="posts", url_path="posts")
    def user_posts(self, request, pk=None):
        qs = self.get_queryset()
        user = get_object_or_404(qs, pk=pk)
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
    def user_feed(self, request, pk=None):
        user_qs = self.get_queryset()
        user = get_object_or_404(user_qs, pk=pk)

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
    def user_liked(self, request, pk=None, post_pk=None):
        user_qs = self.get_queryset()
        user = get_object_or_404(user_qs, pk=pk)

        post_qs = Post.objects.all()
        post = get_object_or_404(post_qs, pk=post_pk)

        is_liked = post.likes.filter(id=user.id).exists()

        return Response({"is_liked": is_liked})
