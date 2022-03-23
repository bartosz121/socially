import pytest

from profiles.models import Profile
from accounts.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_object_name():
    user = CustomUserFactory(email="user123@email.com")
    expected_obj_name = f"#{user.profile.pk} - {user.profile.username}"

    assert str(user.profile) == expected_obj_name


@pytest.mark.django_db
def test_following_count(user):
    test_user1 = CustomUserFactory()
    test_user2 = CustomUserFactory()

    user.profile.following.add(test_user1.profile)
    user.profile.following.add(test_user2.profile)

    expected_value = 2

    assert user.profile.get_following_count() == expected_value


@pytest.mark.django_db
def test_followers_count(user):
    test_user1 = CustomUserFactory()
    test_user2 = CustomUserFactory()

    test_user1.profile.following.add(user.profile)
    test_user2.profile.following.add(user.profile)

    expected_value = 2

    assert user.profile.get_followers_count() == expected_value


# ProfileQuerySet
FOLLOWERS_TEST_COUNT = 3


@pytest.mark.django_db
def test_with_followers_count(user):
    followers = [CustomUserFactory() for _ in range(FOLLOWERS_TEST_COUNT)]

    for f in followers:
        user.profile.followers.add(f.profile)

    user_qs = (
        Profile.objects.all().with_followers_count().filter(user=user).first()
    )

    assert user_qs.followers_count == FOLLOWERS_TEST_COUNT


@pytest.mark.django_db
def test_follow_suggestions(user):
    users_following = [
        CustomUserFactory() for _ in range(FOLLOWERS_TEST_COUNT)
    ]

    users_not_following = [
        CustomUserFactory() for _ in range(FOLLOWERS_TEST_COUNT)
    ]

    for u in users_following:
        user.profile.followers.add(u.profile)

    qs = Profile.objects.all().get_follow_suggestions(user.profile)

    assert all([u.profile in qs for u in users_not_following])
