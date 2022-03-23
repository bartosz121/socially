import pytest
from rest_framework.test import APIClient

from .factories import CustomUserFactory

USER_EMAIL = "johndoe@email.com"


@pytest.fixture
def user():
    return CustomUserFactory(email=USER_EMAIL)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user=user)
    yield client
    client.logout()
