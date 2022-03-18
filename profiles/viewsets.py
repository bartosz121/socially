from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import CustomUser
from api.permissions import IsAuthorOrIsStaffOrReadOnly
from api.utils import get_paginated_queryset_response
from .models import Profile
from .serializers import ProfileSerializer, ProfileBasicSerializer


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Profile viewset
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffOrReadOnly,
    ]

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
        queryset = CustomUser.objects.all()

        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user.profile)
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
            ProfileBasicSerializer,
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
            ProfileBasicSerializer,
        )
