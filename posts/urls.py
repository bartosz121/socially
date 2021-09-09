from django.urls import path
from .views import home_view, PostDetailView

app_name = "posts"

urlpatterns = [
    path("", home_view, name="home-view"),
    path(
        "post/<str:author_username>/<int:pk>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
]
