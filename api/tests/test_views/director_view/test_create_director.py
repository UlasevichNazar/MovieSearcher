import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from movies.models import Director


@pytest.mark.django_db
class TestCreateDirector:
    def test_create_director_with_valid_data_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("director_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Director",
                "description": "Test director description",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        new_director = Director.objects.filter(name="Test Director")
        assert response.status_code == 201
        assert new_director.exists()
        assert new_director[0].description == "Test director description"
        new_director[0].image.delete()
        new_director[0].delete()

    def test_create_director_with_valid_data_by_manager(self, api_client, manager):
        api_client.force_authenticate(manager)
        url = reverse("director_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Director",
                "description": "Test director description",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        new_director = Director.objects.filter(name="Test Director")
        assert response.status_code == 201
        assert new_director.exists()
        assert new_director[0].description == "Test director description"
        new_director[0].image.delete()
        new_director[0].delete()

    def test_create_director_with_missing_required_fields(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("director_create")
        data = {"description": "Test description"}

        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Director.objects.filter(description="Test description").exists()

    def test_create_director_permission_false(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("director_create")
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test Director",
                "description": "Test director description",
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
