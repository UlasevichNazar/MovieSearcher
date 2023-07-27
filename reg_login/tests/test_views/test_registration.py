import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from reg_login.views import Register


@pytest.mark.django_db
class TestRegister:
    def test_valid_user_registration(self, client):
        url = reverse("django_register")
        # Arrange
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "free_mailing_list": True,
        }

        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 302
        assert get_user_model().objects.filter(username="testuser").exists()

    def test_unchecked_mailing_list(self, client):
        url = reverse("django_register")
        # Arrange
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "free_mailing_list": False,
        }

        # Act
        response = client.post(url, data=data)
        # Assert
        user = get_user_model().objects.filter(username="testuser")
        assert response.status_code == 302
        assert user.exists()
        assert user[0].free_mailing_list == False

    def test_register_view_post_form_invalid(self, factory):
        # Arrange
        url = reverse("django_register")
        data = {
            "username": "testuser",
            "email": "invalid_email",
            "password1": "testpassword",
            "password2": "different_password",
            "free_mailing_list": False,
        }
        request = factory.post(url, data=data)
        # Act
        response = Register.as_view()(request)
        # Assert
        assert response.status_code == 200
        assert "Регистрация" in response.rendered_content
        assert "This field is required." not in response.rendered_content

    def test_existing_username(self, client, user):
        # Arrange
        user.save()
        url = reverse("django_register")
        data = {
            "username": "Test",
            "email": "test11111@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "free_mailing_list": True,
        }

        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert (
            "Пользователь с таким Никнейм уже существует." in response.content.decode()
        )

    def test_existing_email(self, client, user):
        # Arrange
        user.save()
        url = reverse("django_register")
        data = {
            "username": "testuser1",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "free_mailing_list": True,
        }

        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert "Пользователь с таким Email уже существует." in response.content.decode()
