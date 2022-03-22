from unittest.case import expectedFailure
from django.test import TestCase
from posts.models import Post
from posts.tests.factories import PostFactory, PostFactoryWithParent
from accounts.tests.factories import CustomUserFactory
from profiles.models import Profile
from profiles.tests.factories import ProfileFactory


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 'main' post
        cls.test_user = CustomUserFactory(email="user@factory.com")
        cls.post = PostFactory(author=cls.test_user)

        # Create comments
        cls.comments = tuple(
            PostFactoryWithParent(parent=cls.post) for _ in range(5)
        )

        # Create post 'likers'
        cls.likers = tuple(CustomUserFactory() for _ in range(3))
        cls.post.likes.add(*cls.likers)

    def test_object_name(self):
        expected_object_name = (
            f"{self.post.pk} by {self.test_user.profile.username}"
        )
        self.assertEqual(str(self.post), expected_object_name)

    def test_like_count(self):
        expected_like_count = len(self.likers)
        self.assertEqual(
            self.post.like_count,
            expected_like_count,
        )

    def test_comment_count(self):
        expected_comment_count = len(self.comments)
        self.assertEqual(
            self.post.get_comment_count(),
            expected_comment_count,
        )
