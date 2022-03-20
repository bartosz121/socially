from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ..viewsets import UserViewSet

user_posts = UserViewSet.as_view(
    {
        "get": "user_posts",
    }
)

user_feed = UserViewSet.as_view(
    {
        "get": "user_feed",
    }
)

user_liked = UserViewSet.as_view(
    {
        "get": "user_liked",
    }
)


urlpatterns = format_suffix_patterns(
    [
        path("users/<int:pk>/posts/", user_posts, name="posts"),
        path("users/<int:pk>/feed/", user_feed, name="feed"),
        path("users/<int:pk>/liked/<int:post_pk>/", user_liked, name="liked"),
    ]
)
