from django.urls import path, re_path
from .views import (
    ProfileDetailView,
    HandleFollow,
    # htmx
    follow_suggestions_hx,
    profile_followers_hx,
    profile_following_hx,
)

app_name = "profiles"

urlpatterns = [
    # HTMX
    path(
        "follow_suggestions_hx/",
        follow_suggestions_hx,
        name="follow-suggestions-hx",
    ),
    path(
        "profile_followers_hx/<int:pk>",
        profile_followers_hx,
        name="profile-followers-hx",
    ),
    path(
        "profile_following_hx/<int:pk>",
        profile_following_hx,
        name="profile-following-hx",
    ),
    # Standard
    path(
        "<slug:username>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "handlefollow/<int:profile_pk>",
        HandleFollow.as_view(),
        name="handle-follow",
    ),
]
