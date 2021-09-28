from django.urls import path
from .views import HomeView, PostDetailView, HandleLike

app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("handlelike/<int:pk>", HandleLike.as_view(), name="handle-like"),
]
