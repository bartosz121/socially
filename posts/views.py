from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.http import require_http_methods
from .models import Post
from .forms import PostForm, ReplyForm
from .helpers import PaginableView

# Create your views here.


class HomeView(PaginableView):
    template_name = "posts/main.html"

    def get_context_data(self, **kwargs):
        qs = Post.objects.all().order_by("-created")
        kwargs["posts"] = self.get_paginator_page(qs, 5)
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


class PostDetailView(PaginableView):
    http_method_names = ["get", "post"]
    template_name = "posts/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        parent_post = get_object_or_404(Post, pk=pk)
        kwargs["post"] = parent_post
        comments_qs = Post.objects.filter(parent=parent_post).order_by(
            "-created"
        )
        kwargs["comments"] = self.get_paginator_page(comments_qs, 5)

        if "reply_form" not in kwargs:
            kwargs["reply_form"] = ReplyForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, pk, *args, **kwargs):
        context = {}
        reply_form = ReplyForm(request.POST, request.FILES)
        reply_form.is_valid()
        if reply_form.is_valid():
            reply_form.instance.author = request.user.profile
            reply_form.instance.parent = get_object_or_404(Post, pk=pk)
            reply_form.save()
            messages.success(request, "Reply posted!")
            return redirect(reverse("posts:post-detail", kwargs={"pk": pk}))
        else:
            messages.error(request, "Something went wrong...")
            context["reply_form"] = reply_form

        return render(
            request, self.template_name, self.get_context_data(**context)
        )


class PostUpdateView(UpdateView):
    model = Post
    template_name = "posts/post_update.html"
    fields = ["body", "picture"]
    exclude = ["parent", "author", "liked", "created", "updated"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.profile != context["post"].author:
            raise PermissionDenied
        return context


@login_required
@require_http_methods(["DELETE"])
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.profile != post.author and not request.user.is_staff:
        raise PermissionDenied

    post.delete()
    response = {"result": "deleted", "redirect": False}

    if request.GET.get("redirect") == "True":
        response["redirect"] = True

    return JsonResponse(response, safe=False)


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
        post = Post.objects.filter(id=pk)
        if not post:
            return redirect("posts:home-view")
        return redirect(
            reverse("posts:post-detail", kwargs={"pk": post[0].pk})
        )
