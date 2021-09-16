from django.urls import path, re_path
from .views import ProfileDetailView, HandleFollow

app_name = "profiles"

urlpatterns = [
    path(
        "<slug:username>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "handlefollow/<int:pk>", HandleFollow.as_view(), name="handle-follow"
    ),
]
