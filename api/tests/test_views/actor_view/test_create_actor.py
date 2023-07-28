import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from movies.models import Actor


@pytest.mark.django_db
class TestCreateActor:
    def test_create_actor_with_valid_data_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("actors_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Actor",
                "description": "Test actor description",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        new_actor = Actor.objects.filter(name="Test Actor")
        assert response.status_code == 201
        assert new_actor.exists()
        assert new_actor[0].description == "Test actor description"
        new_actor[0].image.delete()
        new_actor[0].delete()

    def test_create_actor_with_valid_data_by_manager(self, api_client, manager):
        api_client.force_authenticate(manager)
        url = reverse("actors_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Actor",
                "description": "Test actor description",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        new_actor = Actor.objects.filter(name="Test Actor")
        assert response.status_code == 201
        assert new_actor.exists()
        assert new_actor[0].description == "Test actor description"
        new_actor[0].image.delete()
        new_actor[0].delete()

    def test_create_actor_with_missing_required_fields(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("actors_create")
        data = {"description": "Test description"}

        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Actor.objects.filter(description="Test description").exists()

    def test_create_actor_permission_false(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("actors_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Actor",
                "description": "Test actor description",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )
