from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import UpdateView, ListView
from django.views.decorators.http import require_http_methods
from profiles.models import Profile
from .models import Post
from .forms import PostForm, ReplyForm, SearchForm
from .decorators import get_paginator_hx

# Create your views here.

# HTMX views
# Not sure if there is some name convention
# for now im using the following:
#   _hx - (GET only) get http fragment


def post_hx(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return TemplateResponse(request, "posts/post.html", {"post": post})


@get_paginator_hx("htmx/_hx/posts_hx.html")
def post_comments_hx(request, pk):
    post = get_object_or_404(Post, pk=pk)
    qs = post.get_comments()
    return qs


@get_paginator_hx("htmx/_hx/posts_hx.html")
def posts_hx(request):
    qs = Post.objects.all().order_by("-created")
    return qs


@get_paginator_hx("htmx/_hx/posts_hx.html")
def posts_by_user_hx(request, pk):
    author = get_object_or_404(Profile, pk=pk)
    qs = Post.objects.filter(author=author).order_by("-created")
    return qs


@get_paginator_hx("htmx/_hx/search/search_post_list_hx.html")
def search_post_query_hx(request, query):
    qs = Post.objects.filter(body__search=query).order_by("-created")
    return qs


def popular_posts_hx(request):
    most_replies_posts = sorted(
        Post.objects.all(), key=lambda x: x.comment_count, reverse=True
    )[:7]

    return TemplateResponse(
        request,
        "htmx/_hx/popular_posts_hx.html",
        {"most_replies_posts": most_replies_posts},
    )


def search_form_hx(request):
    search_form = SearchForm()
    return TemplateResponse(
        request, "htmx/_hx/search_form_hx.html", {"search_form": search_form}
    )


def follow_suggestions_hx(request):
    if request.user.is_authenticated:
        follow_suggestions = request.user.profile.get_follow_suggestions()
    else:
        # TODO get 'popular' accounts
        # for now get random
        follow_suggestions = Profile.objects.order_by("?")[:5]

    return TemplateResponse(
        request,
        "htmx/_hx/follow_suggestions_hx.html",
        {"follow_suggestions": follow_suggestions},
    )


# Standard views


class SearchView(View):
    template_name = "posts/search.html"

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        query = None
        profiles = None
        if "query" in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]
                profiles = Profile.objects.filter(username__icontains=query)[
                    :5
                ]

        return render(
            request,
            "posts/search.html",
            {
                "form": form,
                "query": query,
                "profiles": profiles,
            },
        )


class HomeView(View):
    template_name = "posts/main.html"

    def get_context_data(self, **kwargs):
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


class PostDetailView(View):
    http_method_names = ["get", "post"]
    template_name = "posts/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        parent_post = get_object_or_404(Post, pk=pk)
        kwargs["post"] = parent_post

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


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "posts/post_update.html"
    fields = ["body", "picture"]
    exclude = ["parent", "author", "liked", "created", "updated"]

    def test_func(self):
        post = self.get_object()
        return post.author.user == self.request.user


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
    def post(self, request, post_pk, *args, **kwargs):
        # TODO user can delete post and it will still be visible meanwhile user likes -> this throws error
        post = Post.objects.get(pk=post_pk)
        response = {}

        if not post.get_user_liked(request.user):
            response["value"] = "like"
            post.liked.add(request.user)
        else:
            response["value"] = "dislike"
            post.liked.remove(request.user)

        response["likes"] = post.like_count

        return JsonResponse(response, safe=False)

    def get(self, request, post_pk, *args, **kwargs):
        post = Post.objects.filter(id=post_pk)
        if not post:
            return redirect("posts:home-view")
        return redirect(
            reverse("posts:post-detail", kwargs={"pk": post[0].pk})
        )


class ExploreView(View):
    template_name = "posts/explore.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
