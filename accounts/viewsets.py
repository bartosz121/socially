from django.shortcuts import get_object_or_404
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

    @action(
        methods=["GET"],
        detail=True,
        url_name="feed",
        url_path="feed",
        permission_classes=[IsUserOrIsStaff],
    )
    def user_feed(self, request, pk=None):
        user_qs = CustomUser.objects.all()
        user = get_object_or_404(user_qs, pk=pk)

        feed_qs = Post.objects.user_feed(user)

        return get_paginated_queryset_response(
            self.paginator, request, feed_qs, PostSerializer
        )

    @action(
        methods=["GET"],
        detail=True,
        url_name="liked",
        permission_classes=[IsUserOrIsStaff],
    )
    def user_liked(self, request, pk=None, post_pk=None):
        user_qs = CustomUser.objects.all()
        user = get_object_or_404(user_qs, pk=pk)

        post_qs = Post.objects.all()
        post = get_object_or_404(post_qs, pk=post_pk)

        is_liked = post.likes.filter(id=user.id).exists()

        return Response({"is_liked": is_liked})
