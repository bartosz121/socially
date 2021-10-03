from django.test import TestCase

from accounts.models import CustomUserManager, CustomUser
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
    @classmethod
    def setUpTestData(cls):
        CustomUser._default_manager.create_user(
            email="user@email.com", password="Password123!@#"
        )
        cls.user = CustomUser.objects.get(email="user@email.com")

    def test_object_name(self):
        expected_object_name = f"User #{self.user.pk} {self.user.email}"
        self.assertEqual(str(self.user), expected_object_name)
