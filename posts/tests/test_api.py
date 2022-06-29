import pytest
from django.conf import settings

from posts.models import Post
from posts.tests.factories import PostFactory


@pytest.mark.django_db
def test_create_post(auth_client):
    post_data = {"body": "Hello world"}
    response = auth_client.post("/api/v1/posts/", post_data)

    data = response.data

    assert response.status_code == 201
    assert data["body"] == post_data["body"]


@pytest.mark.django_db
def test_create_post_no_authentication(client):
    post_data = {"body": "Hello world"}

    response = client.post("/api/v1/posts/", post_data)


    assert response.status_code == 401


@pytest.mark.django_db
def test_create_post_bad_request_body_max_length(auth_client):
    post_data = {"body": "x" * (settings.MAX_POST_LENGTH + 50)}

    response = auth_client.post("/api/v1/posts/", post_data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_like(auth_client):
    post = PostFactory()

    # like
    response = auth_client.post(
        f"/api/v1/posts/{post.id}/like/", {"action": "like"}
    )
    data = response.data

    assert response.status_code == 200
    assert data["like_count"] == 1

    # dislike
    response = auth_client.post(
        f"/api/v1/posts/{post.id}/like/", {"action": "dislike"}
    )

    data = response.data

    assert response.status_code == 200
    assert data["like_count"] == 0


@pytest.mark.django_db
def test_post_comments(client):
    main_post = PostFactory()

    comments = []

    # comments
    for _ in range(3):
        comments.append(PostFactory(parent=main_post))

    response = client.get(f"/api/v1/posts/{main_post.id}/comments/")

    results = response.data["results"]

    assert response.status_code == 200
    assert len(results) == len(comments)


@pytest.mark.django_db
def test_most_commented(client):
    main_post = PostFactory()

    comments = []

    # comments
    for _ in range(5):
        comments.append(PostFactory(parent=main_post))

    response = client.get(f"/api/v1/posts/most-commented/")

    most_commented_post = response.data[0]
    print(main_post)

    assert response.status_code == 200
    assert most_commented_post["id"] == main_post.id


@pytest.mark.django_db
def test_destroy_post(user, auth_client):
    post = PostFactory(author=user)

    response = auth_client.delete(f"/api/v1/posts/{post.id}/")

    assert response.status_code == 204

    qs = Post.objects.filter(id=post.id)

    assert qs.exists() == False


@pytest.mark.django_db
def test_destroy_post_permission(auth_client):
    post = PostFactory()

    response = auth_client.delete(f"/api/v1/posts/{post.id}/")

    assert response.status_code == 403
