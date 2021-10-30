from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.template.response import TemplateResponse


def get_posts_paginator_hx(func):
    """Get 'posts_hx.html' with paginator from queryset; used in htmx infinite scroll"""

    def wrap(request, *args, **kwargs):
        qs = func(request, *args, **kwargs)
        page = request.GET.get("page", 1)
        hx_get_url = request.build_absolute_uri(
            request.path
        )  # used in posts_hx.html to get next page
        paginator = Paginator(qs, 10)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if len(posts) == 0:
            return HttpResponse("<h3>Posts not found</h3>")

        return TemplateResponse(
            request,
            "htmx/_hx/posts_hx.html",
            {"posts": posts, "hx_get_url": hx_get_url},
        )

    return wrap
