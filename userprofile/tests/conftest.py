import datetime

import pytest
from django.test.client import RequestFactory

from user.models import User
from userprofile.models import Profile


@pytest.fixture
def user() -> User:
    user = User.objects.create_user(
        username="testuser",
        email="test@test.com",
        password="testtest123321",
        free_mailing_list=False,
        first_name="Test",
        last_name="User",
        birthday=datetime.date(1990, 1, 1),
        is_active=True,
        is_superuser=False,
    )
    return user


@pytest.fixture
def profile(user) -> Profile:
    profile = Profile.objects.create(
        user=user, bio="test bio", profile_pic="test_profile_pic.jpg"
    )
    return profile


@pytest.fixture
def factory():
    return RequestFactory()
