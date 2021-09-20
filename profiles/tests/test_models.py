from unittest.case import expectedFailure
from django.test import TestCase
from django.test.testcases import _AssertNumQueriesContext

from profiles.models import Profile
from posts.models import Post
from accounts.models import CustomUser


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user with profile
        # following 2 other users, 3 followers and 2 posts
        user = CustomUser._default_manager.create_user_with_profile(
            email="profileModelTest@email.com", password="Password123!@#"
        )
        cls.profile = user.profile

        # Dummy users
        dummy1 = CustomUser._default_manager.create_user_with_profile(
            email="dummy1@email.com", password="Password123!@#"
        )
        dummy2 = CustomUser._default_manager.create_user_with_profile(
            email="dummy2@email.com", password="Password123!@#"
        )
        dummy3 = CustomUser._default_manager.create_user_with_profile(
            email="dummy3@email.com", password="Password123!@#"
        )

        # Add followers
        dummy1.profile.following.add(user)
        dummy2.profile.following.add(user)
        dummy3.profile.following.add(user)
        cls.followers = [
            dummy1.profile,
            dummy2.profile,
            dummy3.profile,
        ]

        # Test User follows 2 dummy users
        cls.profile.following.add(dummy1)
        cls.profile.following.add(dummy2)
        cls.following = [
            dummy1,
            dummy2,
        ]

        # Create Posts
        post1 = Post.objects.create(author=cls.profile, body="Post 1 body")
        post2 = Post.objects.create(author=cls.profile, body="Post 2 body")
        cls.posts = [post1, post2]

    def test_object_name(self):
        expected_object_name = (
            f"#{self.profile.user.pk} - {self.profile.username}"
        )
        self.assertEqual(str(self.profile), expected_object_name)

    def test_posts_count(self):
        expected_posts_count = len(self.posts)
        self.assertEqual(self.profile.posts_count, expected_posts_count)

    def test_following_count(self):
        expected_following_count = len(self.following)
        self.assertEqual(
            self.profile.following_count, expected_following_count
        )

    def test_followers_count(self):
        expected_followers_count = len(self.followers)
        self.assertEqual(
            self.profile.followers_count, expected_followers_count
        )

    # TODO test get absolute url here

    def test_get_posts(self):
        expected_posts = self.posts
        expected_posts.reverse()  # order '-created'
        self.assertEqual(list(self.profile.get_posts()), expected_posts)

    def test_get_user_follow_status(self):
        # brand new dummy to test not following
        not_following_user = (
            CustomUser._default_manager.create_user_with_profile(
                email="notFollowing@email.com", password="Password123!@#"
            )
        )
        self.assertTrue(self.profile.get_user_follow_status(self.following[0]))
        self.assertFalse(
            self.profile.get_user_follow_status(not_following_user)
        )
