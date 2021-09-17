from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post
from .forms import PostForm

# Create your views here.


class HomeView(View):
    template_name = "posts/main.html"

    def get_context_data(self, **kwargs):
        kwargs["posts"] = Post.objects.all().order_by("-created")
        if "form" not in kwargs:
            kwargs["form"] = PostForm()
        return kwargs

    def post(self, request, *args, **kwargs):
        context = {}

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user.profile
            form.save()
            messages.success(request, "Posted!")
            return redirect("posts:home-view")
        else:
            messages.error(request, "Something went wrong...")
            context["form"] = form

        return render(
            request, self.template_name, self.get_context_data(**context)
        )

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


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
