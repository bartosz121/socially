from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils import get_paginated_queryset_response
from api.permissions import IsAuthorOrIsStaffOrReadOnly
from .serializers import PostSerializer, PostLikeSerializer
from .models import Post


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for listing, retrieving, destroying and liking posts
    """

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "like":
            serializer_class = PostLikeSerializer
        else:
            serializer_class = PostSerializer

        return serializer_class

    def get_permissions(self):
        if self.action in ("list", "retrieve", "post_comments"):
            permission_classes = [
                permissions.IsAuthenticatedOrReadOnly,
            ]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().latest()

        return get_paginated_queryset_response(
            self.paginator, request, queryset, self.get_serializer
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            parent_post = None
            if parent_post_pk := request.data.get("parent_post", False):
                queryset = self.get_queryset()
                parent_post = get_object_or_404(queryset, pk=parent_post_pk)

            serializer.save(author=request.user, parent=parent_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        serializer = self.get_serializer(data=request.data)
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

    @action(
        methods=["GET"], detail=True, url_name="comments", url_path="comments"
    )
    def post_comments(self, request, pk=None, *args, **kwargs):
        post_qs = self.get_queryset()
        post = get_object_or_404(post_qs, pk=pk)
        comments = Post.objects.get_comments(post)

        return get_paginated_queryset_response(
            self.paginator, request, comments, self.get_serializer
        )
