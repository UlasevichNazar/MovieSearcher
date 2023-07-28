import datetime

import pytest
from django.db import IntegrityError

from user.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_valid_input(self, user):
        assert user.username == "testuser"
        assert user.email == "test@test.com"
        assert user.check_password("testtest123321")
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.birthday == datetime.date(1990, 1, 1)
        assert user.free_mailing_list == False
        assert user.is_active == True
        assert user.is_superuser == False

    def test_create_user_with_empty_username(self):
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="",
                email="test@test.com",
                password="testtest123321",
            )

    def test_create_user_with_empty_email(self):
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="testuser",
                email="",
                password="testtest123321",
            )

    def test_update_user_valid_data(self, user):
        user.username = "updating username"
        user.email = "updatingemail@email.com"
        user.save()
        assert User.objects.filter(username="updating username").exists()
        assert User.objects.filter(email="updatingemail@email.com").exists()

    def test_update_username_invalid_data(self, user):
        with pytest.raises(IntegrityError):
            user.username = None
            user.save()

    def test_update_email_invalid_data(self, user):
        with pytest.raises(IntegrityError):
            user.email = None
            user.save()

    def test_delete_user_valid(self, user):
        user.delete()
        assert not User.objects.filter(username="testuser").exists()
