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
        user = CustomUserFactory(email="user@factory.com")
        cls.profile = ProfileFactory(user=user, username="user1")
        cls.post = PostFactory(author=cls.profile)

        # Create comments
        cls.comments = tuple(
            PostFactoryWithParent(parent=cls.post) for _ in range(5)
        )

        # Create post 'likers'
        cls.likers = tuple(ProfileFactory().user for _ in range(3))
        cls.post.liked.add(*cls.likers)

    def test_object_name(self):
        expected_object_name = f"{self.post.pk} by {self.profile.username}"
        self.assertEqual(str(self.post), expected_object_name)

    def test_get_liked(self):
        self.assertEqual(tuple(self.post.get_liked()), self.likers)

    def test_get_comments(self):
        self.assertEqual(tuple(self.post.get_comments()), self.comments)

    def test_get_user_liked(self):
        no_like_user = ProfileFactory()
        self.assertFalse(self.post.get_user_liked(no_like_user))
        self.assertTrue(self.post.get_user_liked(self.likers[0]))

    def test_like_count(self):
        expected_like_count = len(self.likers)
        self.assertEqual(
            self.post.like_count,
            expected_like_count,
        )

    def test_comment_count(self):
        expected_comment_count = len(self.comments)
        self.assertEqual(
            self.post.comment_count,
            expected_comment_count,
        )

    def test_author_username(self):
        expected_author_username = self.profile.username
        self.assertEqual(self.post.author_username, expected_author_username)
