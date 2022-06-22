from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from random import randint, choices

from accounts.models import CustomUser

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Random_follow running...")
        users_qs = CustomUser.objects.all()

        USERS_COUNT = users_qs.count()
        self.stdout.write(f"USERS IN DB: {USERS_COUNT}")

        for user in users_qs:
            n_following = randint(USERS_COUNT // 3, USERS_COUNT)
            self.stdout.write(
                f"User: {user.profile.username} will follow {n_following} profiles!"
            )

            following_users = choices(users_qs, k=n_following)

            for follow_user in following_users:
                user.profile.following.add(follow_user.profile)

            self.stdout.write("DONE")
