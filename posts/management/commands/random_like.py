from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from random import randint, choices

from posts.models import Post
from accounts.models import CustomUser

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Random_like running...")
        users_qs = CustomUser.objects.all()

        posts_qs = Post.objects.all()

        USERS_COUNT = users_qs.count()

        for post in posts_qs:
            n_likes = randint(0, USERS_COUNT)
            self.stdout.write(
                f"Post #{post.id} will be liked {n_likes} times!"
            )

            like_users = choices(users_qs, k=n_likes)

            for user in like_users:
                post.likes.add(user)

            self.stdout.write("DONE")
