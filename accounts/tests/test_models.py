from django.test import TestCase

from accounts.models import CustomUserManager, CustomUser
from posts.tests.factories import PostFactory
from profiles.models import Profile
from accounts.tests.factories import CustomUserFactory, CustomSuperUserFactory


class CustomUserManagerTest(TestCase):
    def test_email_not_provided(self):
        with self.assertRaises(ValueError, msg="The Email must be set"):
            CustomUser._default_manager.create_superuser(
                email=None, password="Password123!@#"
            )

    def test_create_profile_for_superuser(self):
        CustomUser._default_manager.create_superuser(
            email="superUser@email.com", password="Password123!@#"
        )
        super_user = CustomUser.objects.get(email="superUser@email.com")
        self.assertTrue(Profile.objects.get(user=super_user))

    def test_create_superuser_raises(self):
        with self.assertRaises(
            ValueError, msg="Superuser must have 'is_staff' set to True"
        ):
            CustomUser._default_manager.create_superuser(
                email="superUser@email.com",
                password="Password123!@#",
                is_staff=False,
            )

        with self.assertRaises(
            ValueError, msg="Superuser must have 'is_staff' set to True"
        ):
            CustomUser._default_manager.create_superuser(
                email="superUser@email.com",
                password="Password123!@#",
                is_superuser=False,
            )


class CustomUserModelTest(TestCase):
    TEST_USER_N_POSTS = 4

    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUserFactory(email="user123@user.com")

        # Create TEST_USER_N_POSTS posts
        for _ in range(cls.TEST_USER_N_POSTS):
            PostFactory(author=cls.test_user)

    def test_object_name(self):
        expected_object_name = (
            f"User #{self.test_user.pk} {self.test_user.email}"
        )
        self.assertEqual(str(self.test_user), expected_object_name)

    def test_get_posts_count(self):
        self.assertEqual(
            self.test_user.get_posts_count(), self.TEST_USER_N_POSTS
        )
