from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.template.response import TemplateResponse


def get_paginator_hx(template):
    def decorate(func):
        def wrap(request, *args, **kwargs):
            qs = func(request, *args, **kwargs)
            page = request.GET.get("page", 1)
            hx_get_url = request.path
            paginator = Paginator(qs, 10)

            try:
                result = paginator.page(page)
            except PageNotAnInteger:
                result = paginator.page(1)
            except EmptyPage:
                result = paginator.page(paginator.num_pages)

            if len(result) == 0:
                return HttpResponse("<h3>Result not found</h3>")

            return TemplateResponse(
                request,
                template,
                {"result": result, "hx_get_url": hx_get_url},
            )

        return wrap

    return decorate
