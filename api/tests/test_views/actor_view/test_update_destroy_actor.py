import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from movies.models import Actor


@pytest.mark.django_db
class TestUpdateDestroyActor:
    def test_update_actor_by_admin(self, api_client, actor, superuser):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Actor",
                "description": "Updating Test actor description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        updating_actor = Actor.objects.filter(name="Updating Test Actor")
        assert response.status_code == 200
        assert updating_actor.exists()
        assert updating_actor[0].description == "Updating Test actor description"
        updating_actor[0].image.delete()
        updating_actor[0].delete()

    def test_update_actor_by_manager(self, api_client, actor, manager):
        api_client.force_authenticate(manager)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Actor",
                "description": "Updating Test actor description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        updating_actor = Actor.objects.filter(name="Updating Test Actor")
        assert response.status_code == 200
        assert updating_actor.exists()
        assert updating_actor[0].description == "Updating Test actor description"
        updating_actor[0].image.delete()
        updating_actor[0].delete()

    def test_update_actor_permission_false(self, api_client, user, actor):
        api_client.force_authenticate(user)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Actor",
                "description": "Updating Test actor description",
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

    def test_updating_non_exiting_actor(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/actors/admin/999/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test Actor",
                "description": "Updating Test actor description",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_actor_successfully_by_admin(self, api_client, actor, superuser):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Actor.objects.filter(name="Test Actor").exists()

    def test_delete_actor_successfully_by_manager(self, api_client, actor, manager):
        api_client.force_authenticate(manager)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Actor.objects.filter(name="Test Actor").exists()

    def test_delete_actor_permissions_false(self, api_client, actor, user):
        api_client.force_authenticate(user)
        url = f"/api/v1/actors/admin/{actor.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_non_exiting_actor(self, api_client, actor, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/actors/admin/999/"
        response = api_client.delete(url)
        assert response.status_code == 404
