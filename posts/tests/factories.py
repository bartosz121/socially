import factory
from factory.declarations import SubFactory
from django.conf import settings
from accounts.tests.factories import CustomUserFactory

from posts.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    body = factory.Faker("text", max_nb_chars=settings.MAX_POST_LENGTH)
    author = SubFactory(CustomUserFactory)


class PostFactoryWithParent(PostFactory):
    parent = SubFactory(PostFactory)
