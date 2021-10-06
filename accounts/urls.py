from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, SettingsView

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="registration"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="accounts/registration/logout.html",
        ),
        name="logout",
    ),
]
