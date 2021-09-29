from django.urls import path
from .views import HomeView, PostDetailView, HandleLike, delete_post

app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/delete/<int:pk>", delete_post, name="post-delete"
    ),
    path("handlelike/<int:pk>", HandleLike.as_view(), name="handle-like"),
]
