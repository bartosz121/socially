from django.urls import path
from .views import HomeView, HandleLike

app_name = "posts"

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("handlelike/<int:pk>", HandleLike.as_view(), name="handle-like"),
]
