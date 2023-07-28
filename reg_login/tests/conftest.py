import pytest
from django.test import Client
from django.test.client import RequestFactory

from user.models import User


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user() -> User:
    user = User.objects.create_user(
        username="Test",
        email="test@test.com",
        password="testtest123321",
        free_mailing_list=False,
        is_active=True,
        is_superuser=False,
    )
    return user
