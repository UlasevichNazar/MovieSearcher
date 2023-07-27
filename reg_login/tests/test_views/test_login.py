import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLoginUser:
    def test_successful_login(self, client, user):
        url = reverse("django_login")
        data = {"username": "Test", "password": "testtest123321"}
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert response.url == "/"

    def test_incorrect_credentials(self, client, user):
        url = reverse("django_login")
        data = {"username": "Test1", "password": "testtest123321aa"}
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert (
            "Пожалуйста, введите правильные Никнейм и пароль. Оба поля могут быть чувствительны к регистру."
            in response.content.decode()
        )

    def test_invalid_data(self, client, user):
        url = reverse("django_login")
        data = {"username": "", "password": ""}
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert "Обязательное поле." in response.content.decode()

    def test_login_form_display(self, client):
        url = reverse("django_login")
        response = client.get(url)
        assert response.status_code == 200
        assert "form-control" in response.content.decode()
        assert "Логин" in response.content.decode()
        assert "Пароль" in response.content.decode()
