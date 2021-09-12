from django.shortcuts import render
from django.views.generic.detail import DetailView
from profiles.models import Profile

# Create your views here.


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = context["profile"].get_posts()
        return context
