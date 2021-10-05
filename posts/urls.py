from django.urls import path
from .views import (
    HomeView,
    PostDetailView,
    HandleLike,
    PostUpdateView,
    delete_post,
)

app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/update/<int:pk>", PostUpdateView.as_view(), name="post-update"
    ),
    path("posts/delete/<int:pk>", delete_post, name="post-delete"),
    path("handlelike/<int:post_pk>", HandleLike.as_view(), name="handle-like"),
]
