from pathlib import Path
from typing import List, Tuple
from django.http import Http404
import requests
import random
import uuid
from faker import Faker
from django.core.files import File
from django.core.management.base import BaseCommand, CommandParser
from posts.models import Post
from accounts.models import CustomUser
from posts.tests.factories import PostFactory
from django.contrib.auth import get_user_model

# https://github.com/cyberboysumanjay/Inshorts-News-API
NEWS_CATEGORIES = (
    "all",
    "business",
    "sports",
    "world",
    "politics",
    "technology",
    "startup",
    "entertainment",
    "miscellaneous",
    "hatke",
    "science",
    "automobile",
)

User = get_user_model()


class NewsAPI:
    data = {key: None for key in NEWS_CATEGORIES}

    def _fetch_news(self, category):
        url = f"https://inshortsapi.vercel.app/news?category={category}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"]

            self.data[category] = data
        else:
            raise Http404(f"Cant fetch news from {url!r}")

    def get_news(self, category="all"):
        if category not in NEWS_CATEGORIES:
            raise ValueError(
                f"Wrong news category. Choose from: {NEWS_CATEGORIES!r}"
            )

        if self.data[category] is None:
            self._fetch_news(category)

        return self.data[category]


class Command(BaseCommand):
    """
    Creates posts/comments

    CLI arguments:
        - `-n`: Number of posts to be created
        - `-authors_ids`: IDs of users to be used as authors of posts
        - `-posts-category`: Category of posts to be created. Defaults to 'all'. See `NEWS_CATEGORIES`
        - `-post-id-to-comment`: If passed, post with given id will be used as parent to created posts
    """

    USERS_COUNT = 100
    MAX_POSTS_PER_USER = 15
    faker = Faker()
    news = NewsAPI()

    help = "Populate db with dummy data - users, posts, likes, follows"

    def add_arguments(self, parser: CommandParser) -> None:
        required = parser.add_argument_group("Required arguments")

        required.add_argument(
            "-n",
            type=int,
            help="Number of items to create",
            required=True,
        )
        required.add_argument(
            "-authors-ids",
            nargs="+",
            type=int,
            help="Authors IDs",
            required=True,
        )

        optional = parser.add_argument_group("Optional arguments")

        optional.add_argument(
            "-posts-category",
            type=str,
            help="Create comments to post with this id",
            default="all",
        )

        optional.add_argument(
            "-randomize",
            type=bool,
            help="Create comments to post with this id",
        )

        optional.add_argument(
            "-post-id-to-comment",
            type=int,
            help="Create comments to post with this id",
        )

    def handle(self, *args, **kwargs):
        n = kwargs["n"]
        authors = kwargs["authors_ids"]
        posts_category = kwargs["posts_category"]
        post_id_to_comment = kwargs["post_id_to_comment"]
        randomize = kwargs["randomize"]

        if randomize:
            self.stdout.write("RANDOM MODE")
            self.run_random()
        else:

            self.stdout.write(
                f"Creating {n} {'comments' if post_id_to_comment else 'posts'} "
                f"per {len(authors)} users({authors})..."
            )

            self.create_posts(n, authors, posts_category, post_id_to_comment)
        self.cleanup_downloaded_images()

    def run_random(self):
        users_qs = CustomUser.objects.all()
        posts_qs = Post.objects.all()
        USERS_COUNT = users_qs.count()
        POSTS_COUNT = posts_qs.count() // 2
        news_data = self.news.get_news("science")

        random_posts = random.choices(posts_qs, k=POSTS_COUNT)

        for post in random_posts:
            n_comments = random.randint(0, USERS_COUNT // 3)

            self.stdout.write(
                f"Creating {n_comments} comments for Post #{post.id}"
            )

            comment_authors = random.choices(users_qs, k=n_comments)

            for user in comment_authors:
                profile = user.profile

                self.stdout.write(f"\t\t{profile.username}: Creating posts...")

                src = news_data[random.randrange(0, len(news_data))]

                data = {
                    "image_url": src.get("imageUrl"),
                    "author": user,
                    "body": src.get("content"),
                }

                data["parent_id"] = post.id

                self.create_and_save_post(**data)
                self.stdout.write(
                    self.style.SUCCESS(f"\t\t\tCreated and saved post")
                )

    def create_posts(
        self,
        n,
        authors: List[Tuple[User, CustomUser]],
        post_category,
        post_id_to_comment: int = None,
    ):
        """
        Creates new posts

        If `authors` is None, create `n` new users with `n` posts each

        Choose post category from `NEWS_CATEGORIES`; default is 'all'
        """

        self.stdout.write(f"\tCreating posts...")
        self.stdout.write(f"\tFetching {post_category!r} news...")
        news_data = self.news.get_news(post_category)

        authors = (CustomUser.objects.get(pk=id_) for id_ in authors)

        for user in authors:
            profile = user.profile

            self.stdout.write(f"\t\t{profile.username}: Creating posts...")

            for _ in range(n):
                src = news_data[random.randrange(0, len(news_data))]

                data = {
                    "image_url": src.get("imageUrl"),
                    "author": user,
                    "body": src.get("content"),
                }

                if post_id_to_comment:
                    data["parent_id"] = post_id_to_comment

                self.create_and_save_post(**data)
                self.stdout.write(
                    self.style.SUCCESS(f"\t\t\tCreated and saved post")
                )

    def add_followers(self, user_to_follow, *, n: int):
        pass

    def add_likes(self, post_to_like, *, n: int):
        pass

    def cleanup_downloaded_images(self):
        images_path = Path(__file__).parent / "downloaded"
        if images_path.exists():
            for file in images_path.iterdir():
                Path.unlink(file)
        self.stdout.write("Temporary image files deleted")

    def create_and_save_post(self, image_url=None, **kwargs):
        post = Post(**kwargs)

        if image_url:
            try:
                img_name, img_path = self.download_image(image_url)
            except Http404:
                pass
            else:
                post.picture.save(img_name, File(open(img_path, "rb")))

        post.save()

    def create_post(self, author, body):
        return PostFactory(author=author, body=body)

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
