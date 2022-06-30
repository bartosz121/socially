import pytest
from accounts.models import CustomUser

from accounts.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_follow(user, auth_client):
    test_user = CustomUserFactory()

    # follow
    response = auth_client.post(
        f"/api/v1/profiles/{test_user.profile.username}/follow/",
        {"action": "follow"},
    )
    data = response.data

    assert response.status_code == 200
    assert data["followers_count"] == 1

    # unfollow
    response = auth_client.post(
        f"/api/v1/profiles/{test_user.profile.username}/follow/",
        {"action": "unfollow"},
    )

    data = response.data

    assert response.status_code == 200
    assert data["followers_count"] == 0


@pytest.mark.django_db
def test_following(user, client):
    test_user = CustomUserFactory()

    test_user.profile.followers.add(user.profile)

    response = client.get(f"/api/v1/profiles/{user.profile.username}/following/")
    assert response.status_code == 200

    data = response.data["results"]

    # only one user is being followed
    assert data[0]["user_id"] == test_user.id


@pytest.mark.django_db
def test_followers(user, client):
    test_user = CustomUserFactory()

    user.profile.followers.add(test_user.profile)

    response = client.get(f"/api/v1/profiles/{user.profile.username}/followers/")
    assert response.status_code == 200

    data = response.data["results"]

    # only one user is being followed
    assert data[0]["user_id"] == test_user.id


@pytest.mark.django_db
def test_follow_suggestions(user, client):
    # have to make user follow itself otherwise user profile will be suggested (TODO fix this)
    user.profile.following.add(user.profile)

    expected_suggestions = [
        CustomUserFactory(),
        CustomUserFactory(),
        CustomUserFactory(),
    ]

    expected_ids = [user.id for user in expected_suggestions]

    response = client.get(f"/api/v1/profiles/{user.profile.username}/follow-suggestions/")
    assert response.status_code == 200

    data = response.data

    assert all(
        [
            response_suggestion["user_id"] in expected_ids for response_suggestion in data
        ]
    )


@pytest.mark.django_db
def test_is_user_following(user, client):
    test_user = CustomUserFactory()

    user.profile.following.add(test_user.profile)

    response = client.get(
        f"/api/v1/profiles/{test_user.profile.username}/is-following/{user.profile.username}/"
    )
    assert response.status_code == 200
    assert response.data["is_following"] == True

    # unfollow
    user.profile.following.remove(test_user.profile)
    response = client.get(
        f"/api/v1/profiles/{test_user.profile.username}/is-following/{user.profile.username}/"
    )
    assert response.status_code == 200
    assert response.data["is_following"] == False


@pytest.mark.django_db
def test_most_followers(user, client):
    most_followed_user = CustomUserFactory()

    n_followers = 3
    # add followers to `user` and `most_followed_user`
    for u in (user, most_followed_user):
        for _ in range(n_followers):
            u.profile.followers.add(CustomUserFactory().profile)

        # add 5 more followers to `most_followed_user` in next iteration
        n_followers += 5

    response = client.get(f"/api/v1/profiles/most-followers/")
    assert response.status_code == 200

    data = response.data

    assert data[0]["user_id"] == most_followed_user.id
    assert data[1]["user_id"] == user.id

@pytest.mark.django_db
def test_viewset_list(client):
    PAGINATED_RESULT_ITEM_COUNT = 10

    profiles = [CustomUserFactory().profile for _ in range(15)]
    profiles.reverse()
    profiles_usernames = [profile.username for profile in profiles[:PAGINATED_RESULT_ITEM_COUNT]]

    response = client.get("/api/v1/profiles/")
    assert response.status_code == 200

    data = response.data
    assert data["next"].endswith("?page=2")
    assert data["previous"] is None
    assert data["count"] == len(profiles)

    assert all([expected_username == p["username"] for expected_username, p in zip(profiles_usernames, data["results"])])



@pytest.mark.django_db
def test_viewset_retrieve(client):
    profile = CustomUserFactory().profile
    response = client.get(f"/api/v1/profiles/{profile.username}/")
    assert response.status_code == 200
    assert response.data["username"] == profile.username

@pytest.mark.django_db
def test_follow_stats(client):
    follow_target = CustomUserFactory()

    # 6 followers and 5 following
    for i in range(11):
        user = CustomUserFactory()
        if i % 2 == 0:
            follow_target.profile.followers.add(user.profile)
        else:
            user.profile.followers.add(follow_target.profile)

    response = client.get(f"/api/v1/profiles/{follow_target.profile.username}/follow/count/")
    assert response.status_code == 200

    data = response.data
    assert data["user_id"] == follow_target.id
    assert data["followers"] == 6
    assert data["following"] == 5