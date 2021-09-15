from django.urls import path
from .views import home_view, HandleLike

app_name = "posts"

urlpatterns = [
    path("", home_view, name="home-view"),
    path("handlelike/<int:pk>", HandleLike.as_view(), name="handle-like"),
]
