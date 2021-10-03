import factory
from factory.declarations import SubFactory

from posts.models import Post
from profiles.tests.factories import ProfileFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    body = factory.Faker("text", max_nb_chars=300)
    author = SubFactory(ProfileFactory)


class PostFactoryWithParent(PostFactory):
    parent = SubFactory(PostFactory)
