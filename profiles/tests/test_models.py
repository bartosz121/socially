from django.test import TestCase
from posts.tests.factories import PostFactory
from profiles.models import Profile
from accounts.tests.factories import CustomUserFactory, CustomSuperUserFactory

# from profiles.tests.factories import ProfileFactory, SuperUserProfileFactory


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user with profile
        # following 2 other users, 3 followers and 2 posts
        cls.test_user = CustomUserFactory()

        # Dummy users
        dummy1 = CustomSuperUserFactory()
        dummy2 = CustomUserFactory()
        dummy3 = CustomUserFactory()
        cls.dummy_users = (
            dummy1,
            dummy2,
            dummy3,
        )

        # Add followers
        dummy1.profile.following.add(cls.test_user.profile)
        dummy2.profile.following.add(cls.test_user.profile)
        dummy3.profile.following.add(cls.test_user.profile)

        cls.followers = [
            dummy1,
            dummy2,
            dummy3,
        ]

        # Test User follows 2 dummy users
        cls.test_user.profile.following.add(dummy1.profile)
        cls.test_user.profile.following.add(dummy2.profile)
        cls.following = [
            dummy1,
            dummy2,
        ]

        # Create Posts
        cls.posts = tuple(PostFactory(author=cls.test_user) for _ in range(4))

    def test_object_name(self):
        expected_object_name = (
            f"#{self.test_user.profile.pk} - {self.test_user.profile.username}"
        )
        self.assertEqual(str(self.test_user.profile), expected_object_name)

    def test_following_count(self):
        expected_following_count = len(self.following)
        self.assertEqual(
            self.test_user.profile.get_following_count(),
            expected_following_count,
        )

    def test_followers_count(self):
        expected_followers_count = len(self.followers)
        self.assertEqual(
            self.test_user.profile.get_followers_count(),
            expected_followers_count,
        )
