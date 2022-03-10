from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.viewsets import PostViewSet

app_name = "api"

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls
