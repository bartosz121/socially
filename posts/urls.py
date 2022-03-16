from django.urls import path
from .views import (
    ExploreView,
    HomeView,
    PostDetailView,
    PostUpdateView,
    SearchView,
    # htmx
    post_hx,
    post_comments_hx,
    posts_hx,
    posts_by_user_hx,
    popular_posts_hx,
    search_form_hx,
    search_post_query_hx,
)

app_name = "posts"

urlpatterns = [
    # HTMX
    path("posts/post_hx/<int:pk>", post_hx, name="post-hx"),
    path(
        "posts/post_comments_hx/<int:pk>",
        post_comments_hx,
        name="post-comments-hx",
    ),
    path("posts/posts_hx/", posts_hx, name="posts-hx"),
    path(
        "posts/posts_by_user_hx/<int:pk>",
        posts_by_user_hx,
        name="posts-by-user-hx",
    ),
    path(
        "posts/popular_posts_hx/",
        popular_posts_hx,
        name="popular-posts-hx",
    ),
    path("posts/search_form_hx/", search_form_hx, name="search-form-hx"),
    path(
        "posts/search_post_query_hx/<slug:query>",
        search_post_query_hx,
        name="search-query-hx",
    ),
    # Standard
    path("", HomeView.as_view(), name="home-view"),
    path("explore/", ExploreView.as_view(), name="explore-view"),
    path("search/", SearchView.as_view(), name="search"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/update/<int:pk>", PostUpdateView.as_view(), name="post-update"
    ),
]
