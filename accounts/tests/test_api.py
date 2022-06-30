import pytest
from accounts.tests.factories import CustomUserFactory
from posts.tests.factories import PostFactory


@pytest.mark.django_db
def test_user_posts(user, client):
    user_posts = []
    for _ in range(3):
        user_posts.append(PostFactory(author=user))

    user_posts.reverse()  # for zip in assert

    response = client.get(f"/api/v1/users/{user.profile.username}/posts/")
    assert response.status_code == 200

    result = response.data["results"]

    assert len(result) == len(user_posts)

    assert all(
        [r_obj["id"] == u_obj.id for r_obj, u_obj in zip(result, user_posts)]
    )


@pytest.mark.django_db
def test_user_feed(user, client):
    test_users = [CustomUserFactory() for _ in range(3)]

    # create one post for each user
    p1 = PostFactory(author=test_users[0])
    p2 = PostFactory(author=test_users[1])
    p3 = PostFactory(author=test_users[2])

    # follow only first two users
    test_users[0].profile.followers.add(user.profile)
    test_users[1].profile.followers.add(user.profile)

    expected_user_feed = [p1, p2]
    response = client.get(f"/api/v1/users/{user.profile.username}/feed/")

    assert response.status_code == 200

    result = response.data["results"]

    expected_user_feed.reverse()

    assert all(
        [
            r_obj["id"] == u_obj.id
            for r_obj, u_obj in zip(result, expected_user_feed)
        ]
    )


@pytest.mark.django_db
def test_user_liked(user, client):
    posts = [PostFactory() for _ in range(3)]

    # like first two posts
    posts[0].likes.add(user)
    posts[1].likes.add(user)

    for i, post in enumerate(posts):
        response = client.get(f"/api/v1/users/{user.profile.username}/liked/{post.id}/")
        assert response.status_code == 200

        if i == 2:
            expected_value = False
        else:
            expected_value = True

        assert response.data["is_liked"] == expected_value
