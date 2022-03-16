from django.conf import settings

from posts.permissions import IsAuthorOrIsStaffOrReadOnly
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post

from .serializers import PostLikeSerializer

User = settings.AUTH_USER_MODEL


class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for listing, retrieving, destroying and liking posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffOrReadOnly,
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()

        post = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(post, context={"request": request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=True)
    def like(self, request, pk=None, *args, **kwargs):
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            queryset = self.get_queryset()
            post = get_object_or_404(queryset, pk=pk)

            data = serializer.validated_data
            action = data["action"]

            if action == "like":
                post.likes.add(request.user)
            else:
                # dislike
                post.likes.remove(request.user)

            return Response(
                {"like_count": post.likes.count(), **data},
                status=status.HTTP_200_OK,
            )

    @action(methods=["GET"], detail=True, url_path="is-liked")
    def is_liked(self, request, pk=None, *args, **kwargs):
        post_qs = self.get_queryset()
        post = get_object_or_404(post_qs, pk=pk)

        user = request.user

        is_liked = post.likes.filter(id=user.id).exists()

        return Response({"is_liked": is_liked})
