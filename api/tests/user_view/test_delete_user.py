import pytest

from user.models import User


@pytest.mark.django_db
class TestDeleteUser:
    def test_delete_user_successfully_by_admin(self, api_client, superuser, user):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/user/delete/{user.pk}/"
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not User.objects.filter(username=user.username).exists()

    def test_delete_user_successfully_by_manager(self, api_client, manager, user):
        api_client.force_authenticate(manager)
        url = f"/api/v1/user/delete/{user.pk}/"
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not User.objects.filter(username=user.username).exists()

    def test_delete_user_permission_denied(self, api_client, user):
        api_client.force_authenticate(user)
        url = f"/api/v1/user/delete/{user.pk}/"
        response = api_client.delete(url)

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_non_exiting_user(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/user/delete/999/"
        response = api_client.delete(url)

        assert response.status_code == 404
