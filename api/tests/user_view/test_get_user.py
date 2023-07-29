import pytest
from django.urls import reverse

from user.models import User


@pytest.mark.django_db
class TestGetUser:
    def test_get_users_successfully_by_admin(self, api_client, superuser, user):
        api_client.force_authenticate(superuser)
        url = reverse("all_users")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == User.objects.count()
        assert User.objects.count() == 2

    def test_get_users_successfully_by_manager(self, api_client, manager, user):
        api_client.force_authenticate(manager)
        url = reverse("all_users")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == User.objects.count()
        assert User.objects.count() == 2

    def test_get_user_permission_denied(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("all_users")
        response = api_client.get(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_returns_correct_serializer(self, superuser, api_client):
        api_client.force_authenticate(superuser)
        url = reverse("all_users")
        response = api_client.get(url)

        assert response.status_code == 200
        assert list(response.data[0].keys()) == [
            "id",
            "username",
            "email",
            "free_mailing_list",
        ]
