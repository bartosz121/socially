from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.viewsets import PostViewSet
from profiles.viewsets import ProfileViewSet
from accounts.viewsets import UserViewSet

app_name = "api"

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("profiles", ProfileViewSet, basename="profile")
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls
