from pathlib import Path
from typing import List, Tuple
from django.http import Http404
import requests
import random
import uuid
from faker import Faker
from django.core.files import File
from django.core.management.base import BaseCommand, CommandParser
from accounts.tests.factories import CustomUserFactory
from profiles.models import Profile
from profiles.tests.factories import ProfileFactory
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    USERS_COUNT = 100
    MAX_POSTS_PER_USER = 15
    faker = Faker()

    help = "Populate db with dummy data - users, posts, likes, follows"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("n", type=int, help="Number of items to create")
        parser.add_argument(
            "-authors_ids", nargs="+", type=int, help="Authors IDs"
        )

    def handle(self, *args, **kwargs):
        n = kwargs["n"]

        accounts = self.create_accounts(n)
        self.stdout.write(f"Accounts created!")
        self.stdout.write(f"IDs: {[user.id for user, _ in accounts]}")

    def create_user(self):
        return CustomUserFactory()

    def create_profile(self, user):
        return ProfileFactory(user=user)

    def create_accounts(self, n=10) -> List[Tuple[User, Profile]]:
        """
        Creates `n` brand new accounts
        """

        self.stdout.write(f"Creating {n} accounts...")
        accounts = []
        for _ in range(n):
            # randomize if account should have some random background/profile picture with faker.pybool()
            user, profile = self.create_user_with_profile(
                background=self.faker.pybool(),
                picture=self.faker.pybool(),
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created account - {profile.username}")
            )

            accounts.append((user, profile))

        return accounts

    def create_user_with_profile(self, background=False, picture=False):
        user = self.create_user()
        profile = self.create_profile(user)

        if background:
            prof_bg_name, prof_bg_path = self.get_profile_background()
            profile.profile_background.save(
                prof_bg_name, File(open(prof_bg_path, "rb"))
            )

        if picture:
            prof_pic_name, prof_pic_path = self.get_profile_picture()
            profile.profile_picture.save(
                prof_pic_name, File(open(prof_pic_path, "rb"))
            )

        return user, profile

    def cleanup_downloaded_images(self):
        images_path = Path(__file__).parent / "downloaded"
        if images_path.exists():
            for file in images_path.iterdir():
                Path.unlink(file)
        self.stdout.write("Temporary image files deleted")

    def download_image(self, image_url):
        dest_path = Path(__file__).parent / "downloaded"
        dest_path.mkdir(exist_ok=True)

        img_name = str(uuid.uuid4()).split("-")[0] + ".jpg"
        img_path = dest_path / img_name

        r = requests.get(image_url, stream=True)

        if r.status_code == 200:
            with open(img_path, "wb") as f:
                f.write(r.content)
        else:
            raise Http404()

        return img_name, img_path

    def get_profile_picture(self):
        urls = (
            "https://thispersondoesnotexist.com/image",
            "https://picsum.photos/300",
        )
        url = random.choice(urls)
        return self.download_image(url)

    def get_profile_background(self):
        url = "https://picsum.photos/800/200"
        return self.download_image(url)
