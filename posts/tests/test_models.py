import pytest

from posts.models import Post
from posts.tests.factories import PostFactory
from accounts.tests.factories import CustomUserFactory


# Post model
COMMENT_COUNT_TEST = 3


@pytest.mark.django_db
def test_object_name(user):
    post = PostFactory(author=user)
    expected_obj_name = f"{post.pk} by {user.profile.username}"

    assert str(post) == expected_obj_name


@pytest.mark.django_db
def test_comment_count():
    main_post = PostFactory()

    for _ in range(COMMENT_COUNT_TEST):
        PostFactory(parent=main_post)

    assert main_post.get_comment_count() == COMMENT_COUNT_TEST


# PostQuerySet
@pytest.mark.django_db
def test_latest():
    posts = [PostFactory() for _ in range(3)]
    posts.reverse()

    qs = list(Post.objects.all().latest())

    assert qs == posts


@pytest.mark.django_db
def test_feed(user):
    test_users = [CustomUserFactory() for _ in range(3)]
    expected_feed = []

    for u in test_users:
        user.profile.followers.add(u.profile)
        expected_feed.append(PostFactory(author=u))

    expected_feed.reverse()

    qs = list(Post.objects.all().feed(user))

    assert qs == expected_feed


@pytest.mark.django_db
def test_comments_to():
    main_post = PostFactory()

    comments = [PostFactory(parent=main_post) for _ in range(3)]
    comments.reverse()

    qs = list(Post.objects.all().comments_to(main_post))

    assert qs == comments


@pytest.mark.django_db
def test_by_user(user):
    expected_posts = [PostFactory(author=user) for _ in range(3)]
    expected_posts.reverse()

    # dummy posts
    for _ in range(5):
        PostFactory()

    qs = list(Post.objects.all().by_user(user))

    assert qs == expected_posts
