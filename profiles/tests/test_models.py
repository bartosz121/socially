from django.test import TestCase
from posts.tests.factories import PostFactory
from profiles.models import Profile
from profiles.tests.factories import ProfileFactory, SuperUserProfileFactory


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user with profile
        # following 2 other users, 3 followers and 2 posts
        cls.profile = ProfileFactory()

        # Dummy users
        dummy1 = SuperUserProfileFactory()
        dummy2 = ProfileFactory()
        dummy3 = ProfileFactory()
        cls.dummy_users = (
            dummy1.user,
            dummy2.user,
            dummy3.user,
        )

        # Add followers
        dummy1.following.add(cls.profile.user)
        dummy2.following.add(cls.profile.user)
        dummy3.following.add(cls.profile.user)
        cls.followers = [
            dummy1,
            dummy2,
            dummy3,
        ]

        # Test User follows 2 dummy users
        cls.profile.following.add(dummy1.user)
        cls.profile.following.add(dummy2.user)
        cls.following = [
            dummy1.user,
            dummy2.user,
        ]

        # Create Posts
        cls.posts = tuple(PostFactory(author=cls.profile) for _ in range(4))

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

    def test_get_posts(self):
        expected_posts = self.posts
        self.assertEqual(set(self.profile.get_posts()), set(expected_posts))

    def test_get_user_follow_status(self):
        not_following_user = ProfileFactory().user
        self.assertTrue(self.profile.get_user_follow_status(self.following[0]))
        self.assertFalse(
            self.profile.get_user_follow_status(not_following_user)
        )

    def test_get_following_users_posts(self):
        expected_following_posts = []
        for following in self.following:
            post = PostFactory(author=following.profile)
            expected_following_posts.append(post)

        self.assertEqual(
            set(self.profile.get_following_users_posts()),
            set(expected_following_posts),
        )

    def test_get_follow_suggestions(self):
        # Get difference from all dummy users and following
        # and because get_following_suggestions() return Profile type list
        # get 'Profile' instead of 'CustomUser'
        expected_suggestions = [
            dummy.profile
            for dummy in set(self.dummy_users).difference(set(self.following))
        ]

        self.assertEqual(
            self.profile.get_follow_suggestions(), expected_suggestions
        )

    def test_get_follow_suggestions_with_more_users(self):
        """Test if `get_follow_suggestions` method will return
        3 elements if there are more users in db"""

        for _ in range(5):
            ProfileFactory()

        self.assertEqual(len(self.profile.get_follow_suggestions()), 3)
