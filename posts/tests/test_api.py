import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post
from posts.tests.factories import PostFactory

SMALL_IMAGE = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


@pytest.mark.django_db
def test_create_post(auth_client):
    post_data = {"body": "Hello world"}
    response = auth_client.post("/api/v1/posts/", post_data)

    data = response.data

    assert response.status_code == 201
    assert data["body"] == post_data["body"]

@pytest.mark.django_db
def test_create_post_with_parent(auth_client):
    parent_post = PostFactory()

    post_data = {"body": "Hello world", "parent_post": parent_post.id}
    response = auth_client.post("/api/v1/posts/", post_data)

    data = response.data

    assert response.status_code == 201
    assert data["body"] == post_data["body"]
    assert data["parent_post"]["id"] == parent_post.id


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

@pytest.mark.django_db
def test_viewset_list(client):
    POST_FACTORY_COUNT = 15
    PAGINATED_RESULT_ITEM_COUNT = 10  # TODO hardcoded - fix later; put paginator item count in settings.py

    posts = [PostFactory() for _ in range(POST_FACTORY_COUNT)]
    posts.reverse()

    expected_result_ids_page_1 = [post.id for post in posts[:PAGINATED_RESULT_ITEM_COUNT]]
    expected_result_ids_page_2 = [post.id for post in posts[PAGINATED_RESULT_ITEM_COUNT:]]

    response = client.get("/api/v1/posts/")

    assert response.status_code == 200

    data = response.data
    response_page_1_ids = [post["id"] for post in data["results"]]

    # page 1
    assert data["count"] == len(posts)
    assert data["next"].endswith("?page=2")
    assert data["previous"] is None
    assert len(data["results"]) == PAGINATED_RESULT_ITEM_COUNT
    assert all([expected_id == response_id for expected_id, response_id in zip(expected_result_ids_page_1, response_page_1_ids)])

    # page 2
    response = client.get("/api/v1/posts/?page=2")

    assert response.status_code == 200

    data = response.data
    response_page_2_ids = [post["id"] for post in data["results"]]

    expected_page_2_len = POST_FACTORY_COUNT - PAGINATED_RESULT_ITEM_COUNT
    assert data["next"] is None
    assert data["previous"].endswith("/api/v1/posts/")
    assert len(data["results"]) == expected_page_2_len
    assert all([expected_id == response_id for expected_id, response_id in zip(expected_result_ids_page_2, response_page_2_ids)])


@pytest.mark.django_db
def test_viewset_update(auth_client):
    post_data = {"body": "Hello world", "picture_url": SimpleUploadedFile("test_image.jpg", content=SMALL_IMAGE, content_type='image/jpeg')}
    response = auth_client.post("/api/v1/posts/", post_data, format="multipart")
    assert response.status_code == 201
    assert response.data["picture_url"]

    # testing perform_update()
    updated_post_data = {"body": "updated"}
    response = auth_client.post("/api/v1/posts/", updated_post_data)
    assert response.status_code == 201
    assert response.data["body"] == updated_post_data["body"]
    assert response.data["picture_url"] is None


@pytest.mark.django_db
def test_viewset_retrieve(client):
    post = PostFactory()

    response = client.get(f"/api/v1/posts/{post.id}/")
    assert response.status_code == 200

    data = response.data
    assert data["id"] == post.id