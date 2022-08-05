from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated


from accounts.models import CustomUser
from posts.decorators import get_paginator_hx
from profiles.serializers import ProfileUpdateSerializer
from .models import Profile


# HTMX
@get_paginator_hx("htmx/_hx/profiles/profile_list_hx.html")
def profile_followers_hx(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    qs = profile.get_followers()
    return qs


@get_paginator_hx("htmx/_hx/profiles/profile_list_hx.html")
def profile_following_hx(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    qs = profile.get_following_profiles()
    return qs


def follow_suggestions_hx(request):
    if request.user.is_authenticated:
        follow_suggestions = request.user.profile.get_follow_suggestions()
    else:
        # TODO get 'popular' accounts
        # for now get random
        follow_suggestions = Profile.objects.order_by("?")[:5]

    return TemplateResponse(
        request,
        "htmx/_hx/follow_suggestions_hx.html",
        {"follow_suggestions": follow_suggestions},
    )


# Standard


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"


class HandleFollow(LoginRequiredMixin, View):
    def post(self, request, profile_pk, *args, **kwargs):
        calling_user = CustomUser.objects.get(pk=request.user.pk)
        target_user = CustomUser.objects.get(pk=profile_pk)
        response = {}

        if not calling_user.profile.get_user_follow_status(target_user):
            response["value"] = "follow"
            calling_user.profile.following.add(target_user)
        else:
            response["value"] = "unfollow"
            calling_user.profile.following.remove(target_user)

        response["followers"] = target_user.profile.followers_count

        return JsonResponse(response, safe=False)

    def get(self, request, profile_pk, *args, **kwargs):
        user = CustomUser.objects.filter(id=profile_pk)
        if not user:
            return redirect("posts:home-view")
        return redirect(
            reverse(
                "profiles:profile-detail",
                kwargs={"username": user[0].profile.username},
            )
        )


class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

    def get_queryset(self):
        return Profile.objects.none()

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
