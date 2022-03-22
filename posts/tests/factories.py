import factory
from factory.declarations import SubFactory
from accounts.tests.factories import CustomUserFactory

from posts.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    body = factory.Faker("text", max_nb_chars=300)
    author = SubFactory(CustomUserFactory)


class PostFactoryWithParent(PostFactory):
    parent = SubFactory(PostFactory)
