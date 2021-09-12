from django.urls import path, re_path
from .views import ProfileDetailView

app_name = "profiles"

urlpatterns = [
    path(
        r"<slug:username>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
]
