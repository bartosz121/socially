from django.urls import path, include
from django.conf import settings

from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
)


from posts.viewsets import PostViewSet
from profiles.viewsets import ProfileViewSet
from accounts.viewsets import UserViewSet
from accounts.views import RegisterView, UserDetailsView, EmailChangeView


app_name = "api"

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("profiles", ProfileViewSet, basename="profile")
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls

urlpatterns += [
    path("profiles/", include("profiles.urls")),
    path(
        "accounts/email/change/",
        EmailChangeView.as_view(),
        name="change_email",
    ),
    # dj rest auth
    # URLs that do not require a session or valid token
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("auth/register/", RegisterView.as_view()),
    # URLs that require a user to be logged in with a valid session / token.
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path(
        "auth/password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
]

if getattr(settings, "REST_USE_JWT", False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path(
            "token/refresh/",
            get_refresh_view().as_view(),
            name="token_refresh",
        ),
    ]
