from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import CustomUser
from api.permissions import IsAuthorOrIsStaffOrReadOnly
from api.utils import get_paginated_queryset_response
from .models import Profile
from .serializers import (
    ProfileSerializer,
    ProfileBasicSerializer,
    ProfileFollowSerializer,
)


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Profile viewset
    """

    queryset = Profile.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.action in (
            "followers",
            "following",
            "follow_suggestions",
            "most_followers",
        ):
            serializer_class = ProfileBasicSerializer
        elif self.action == "follow":
            serializer_class = ProfileFollowSerializer
        else:
            serializer_class = ProfileSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        return get_paginated_queryset_response(
            self.paginator,
            request,
            queryset,
            ProfileSerializer,
        )

    def retrieve(self, request, pk=None):
        """Retrieve profile by user id"""
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(profile)

        return Response(serializer.data)

    @action(methods=["GET"], detail=True)
    def following(self, request, pk=None, *args, **kwargs):
        """Returns profiles of users that given profile is following"""
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)

        return get_paginated_queryset_response(
            self.paginator,
            request,
            profile.following.all(),
            self.get_serializer,
        )

    @action(methods=["GET"], detail=True)
    def followers(self, request, pk=None, *args, **kwargs):
        """Returns user followers"""
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)

        return get_paginated_queryset_response(
            self.paginator,
            request,
            profile.followers.all(),
            self.get_serializer,
        )

    @action(methods=["POST"], detail=True)
    def follow(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            queryset = self.get_queryset()
            profile = get_object_or_404(queryset, pk=pk)

            data = serializer.validated_data
            action = data["action"]

            if action == "follow":
                profile.followers.add(request.user.profile)
            else:
                profile.followers.remove(request.user.profile)

            return Response(
                {"followers_count": profile.followers.count(), **data},
                status=status.HTTP_200_OK,
            )

    @action(
        methods=["GET"],
        detail=True,
        url_name="follow-suggestions",
        url_path="follow-suggestions",
    )
    def follow_suggestions(self, request, pk=None, *args, **kwargs):
        qs = self.get_queryset()
        profile = get_object_or_404(qs, pk=pk)
        suggestions = Profile.objects.follow_suggestions(profile)
        serializer = self.get_serializer(
            suggestions, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=True,
        url_name="is-user-following",
        url_path="is-following/(?P<request_user_id>[0-9]+)",
    )
    def is_user_following(self, request, pk=None, request_user_id=None):
        qs = self.get_queryset()
        source_profile = get_object_or_404(qs, pk=pk)
        request_profile = get_object_or_404(qs, pk=request_user_id)

        is_following = source_profile.followers.filter(
            id=request_profile.id
        ).exists()

        return Response({"is_following": is_following})

    @action(
        methods=["GET"],
        detail=False,
        url_name="most-followers",
        url_path="most-followers",
    )
    def most_followers(self, request, *args, **kwargs):
        post_qs = Profile.objects.most_followers()
        serializer = self.get_serializer(post_qs, many=True)

        return Response(serializer.data)
