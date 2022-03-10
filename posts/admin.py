from django.contrib import admin
from django.db.models import Count
from .models import Post, PostLike

# Register your models here.


class PostLikeAdmin(admin.TabularInline):
    model = PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]
    list_display = (
        "id",
        "author",
        "with_picture",
        "short_body",
        "likes",
        "created",
        "updated",
    )

    list_filter = ("author", "likes")
    search_fields = ("body",)
    date_hierarchy = "created"
    ordering = (
        "created",
        "updated",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _likes=Count("likes", distinct=True),
        )
        return queryset

    def likes(self, obj):
        return obj._likes

    likes.admin_order_field = "_likes"

    def short_body(self, obj):
        return f"{obj.body[:15]}..."

    def with_picture(self, obj):
        return bool(obj.picture)
