from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


class Command(BaseCommand):
    USERS_COUNT = 100
    MAX_POSTS_PER_USER = 15
    faker = Faker()

    help = "Like given post `n` times."

    def add_arguments(self, parser: CommandParser) -> None:
        required = parser.add_argument_group("Required arguments")

        required.add_argument(
            "-likes",
            type=int,
            help="Like count",
            required=True,
        )

        required.add_argument(
            "-post-id",
            type=int,
            help="Post ID to like",
            required=True,
        )

    def handle(self, *args, **kwargs):
        like_count = kwargs["likes"]
        post_id = kwargs["post_id"]

        self.like_post(like_count, post_id)
        self.stdout.write(f"Post({post_id}) liked {like_count} time!")

    def like_post(self, like_count, post_id):
        self.stdout.write("Fetching post...")
        post_qs = Post.objects.filter(pk=post_id)
        if not post_qs.exists():
            raise ValueError(f"Post (id: {post_id}) not found!")

        post = post_qs.first()

        users_qs = User.objects.exclude(id__in=post.likes.values_list("id"))

        # Check if there is enough users able to like in db
        users_count = users_qs.count()
        if users_count < like_count:
            raise ValueError(
                f"Not enough users in database!"
                f" Number of users able to like post: {users_count}\n"
                "Use 'create_account' command to create more"
            )

        for user in users_qs:
            post.likes.add(user)
