from django.core.paginator import Paginator
from django.views import View


class PaginableView(View):
    def get_paginator_page(self, queryset, per_page):
        paginator = Paginator(queryset, per_page)
        n_page = self.request.GET.get("page")
        page = paginator.get_page(n_page)
        return page
