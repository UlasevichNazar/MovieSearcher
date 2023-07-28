import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from movies.models import Director


@pytest.mark.django_db
class TestUpdateDestroyDirector:
    def test_update_director_by_admin(self, api_client, director, superuser):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/director/admin/{director.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Director",
                "description": "Updating Test director description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        updating_director = Director.objects.filter(name="Updating Test Director")
        assert response.status_code == 200
        assert updating_director.exists()
        assert updating_director[0].description == "Updating Test director description"
        updating_director[0].image.delete()
        updating_director[0].delete()

    def test_update_director_by_manager(self, api_client, director, manager):
        api_client.force_authenticate(manager)
        url = f"/api/v1/director/admin/{director.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Director",
                "description": "Updating Test director description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        updating_director = Director.objects.filter(name="Updating Test Director")
        assert response.status_code == 200
        assert updating_director.exists()
        assert updating_director[0].description == "Updating Test director description"
        updating_director[0].image.delete()
        updating_director[0].delete()

    def test_update_actor_permission_false(self, api_client, user, director):
        api_client.force_authenticate(user)
        url = f"/api/v1/director/admin/{director.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Director",
                "description": "Updating Test director description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_updating_non_exiting_director(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/director/admin/999/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Director",
                "description": "Updating Test director description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_director_successfully_by_admin(
        self, api_client, director, superuser
    ):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/director/admin/{director.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Director.objects.filter(name="Test").exists()

    def test_delete_director_successfully_by_manager(
        self, api_client, director, manager
    ):
        api_client.force_authenticate(manager)
        url = f"/api/v1/director/admin/{director.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Director.objects.filter(name="Test").exists()

    def test_delete_director_permissions_false(self, api_client, director, user):
        api_client.force_authenticate(user)
        url = f"/api/v1/director/admin/{director.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_non_exiting_director(self, api_client, director, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/director/admin/999/"
        response = api_client.delete(url)
        assert response.status_code == 404
