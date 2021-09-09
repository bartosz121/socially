from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from profiles.models import Profile
from .models import Post

# Create your views here.


def home_view(request):
    if request.user.is_authenticated:
        followed_users_posts = request.user.profile.get_following_users_posts()
        return render(
            request,
            "posts/main.html",
            {"followed_users_posts": followed_users_posts},
        )
    else:
        return render(
            request,
            "posts/main.html",
            {"followed_users_posts": Post.objects.all().order_by("-created")},
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(username=self.kwargs["author_username"])
        profile = Profile.objects.get(user=user)
        return super().get_queryset(*args, **kwargs).filter(author=profile)
