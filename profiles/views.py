from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from accounts.models import CustomUser
from .models import Profile

# Create your views here.


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
