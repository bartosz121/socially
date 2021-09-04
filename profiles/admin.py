from django.contrib import admin
from django.db.models import Count
from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "followers",
        "short_bio",
        "profile_picture",
        "profile_background",
        "created",
        "updated",
    )

    list_filter = ("user",)
    search_fields = ("bio",)
    date_hierarchy = "created"
    ordering = (
        "created",
        "updated",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _followers=Count("following", distinct=True),
        )
        return queryset

    def followers(self, obj):
        return obj._followers

    followers.admin_order_field = "_followers"

    def short_bio(self, obj):
        return obj.bio[:15]
