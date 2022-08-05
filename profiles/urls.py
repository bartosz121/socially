from django.urls import path, re_path
from .views import (
    ProfileUpdateView,
    ProfileDetailView,
    HandleFollow,
    # htmx
    follow_suggestions_hx,
    profile_followers_hx,
    profile_following_hx,
)

app_name = "profiles"

urlpatterns = [
    path(
        "profile/change/", ProfileUpdateView.as_view(), name="profile_change"
    ),
]
