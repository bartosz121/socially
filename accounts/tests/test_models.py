import pytest

from accounts.models import CustomUser
from posts.tests.factories import PostFactory


# CustomUserManagerTest


@pytest.mark.django_db
def test_email_not_provided():
    email = "user@email.com"
    CustomUser._default_manager.create_user(
        email=email, password="Passw0rd!@#"
    )

    user = CustomUser.objects.filter(email=email)

    assert user.exists()


def test_email_not_provided():
    with pytest.raises(ValueError) as excinfo:
        CustomUser._default_manager.create_user(
            email=None, password="Passw0rd!@#"
        )

    assert "The Email must be set" in str(excinfo.value)


@pytest.mark.django_db
def test_create_profile_for_superuser():
    email = "superuser@email.com"
    CustomUser._default_manager.create_superuser(
        email=email, password="passw0rD1@#"
    )

    su = CustomUser.objects.filter(email=email)
    assert su.exists()

    su = su.first()
    assert su.is_superuser


@pytest.mark.django_db
def test_create_superuser_raises():
    email = "superuser@email.com"

    with pytest.raises(ValueError) as excinfo:
        CustomUser._default_manager.create_superuser(
            email=email, password="Passw0rd!@#", is_staff=False
        )

    assert "Superuser must have 'is_staff' set to True" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        CustomUser._default_manager.create_superuser(
            email=email, password="Passw0rd!@#", is_superuser=False
        )

    assert "Superuser must have 'is_superuser' set to True" in str(
        excinfo.value
    )


# CustomUserModelTest
TEST_USER_N_POSTS = 3


@pytest.mark.django_db
def test_object_name(user):
    expected_obj_name = f"User #{user.pk} {user.email}"

    assert str(user) == expected_obj_name


@pytest.mark.django_db
def test_get_posts_count(user):
    for _ in range(TEST_USER_N_POSTS):
        PostFactory(author=user)

    assert user.get_posts_count() == TEST_USER_N_POSTS
