from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.detail import DetailView
from .models import Post

# Create your views here.


def home_view(request):
    if request.user.is_authenticated:
        followed_users_posts = request.user.profile.get_following_users_posts()
        return render(
            request,
            "posts/main.html",
            {"posts": followed_users_posts},
        )
    else:
        return render(
            request,
            "posts/main.html",
            {"posts": Post.objects.all().order_by("-created")},
        )


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "posts/detail.html"

#     def get_queryset(self, *args, **kwargs):
#         user = User.objects.get(username=self.kwargs["author_username"])
#         profile = Profile.objects.get(user=user)
#         return super().get_queryset(*args, **kwargs).filter(author=profile)


class HandleLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # TODO user can delete post and it will still be visible meanwhile user likes -> this throws error
        post = Post.objects.get(pk=pk)
        response = {}

        if not post.get_user_liked(request.user):
            response["value"] = "like"
            post.liked.add(request.user)
        else:
            response["value"] = "dislike"
            post.liked.remove(request.user)

        response["likes"] = post.like_count

        return JsonResponse(response, safe=False)

    def get(self, request, pk, *args, **kwargs):
        # TODO redirect to post detail
        return redirect("posts:home-view")
