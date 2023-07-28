import datetime

import pytest

from user.models import User


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
