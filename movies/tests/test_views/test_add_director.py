import pytest
from django.urls import reverse

from movies.models import Director


@pytest.mark.django_db
class TestAddDirector:
    def test_add_director_valid_form(self, client):
        # Arrange
        url = reverse("add_director")
        data = {
            "name": "Test Director",
            "description": "Test Description",
            "image": "test_image.jpg",
        }
        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert Director.objects.count() == 1
        assert Director.objects.filter(name="Test Director").exists()

    def test_add_director_empty_form(self, client):
        # Arrange
        url = reverse("add_director")

        # Act
        response = client.post(url, data={})
        # Assert
        assert response.status_code == 200
        assert Director.objects.count() == 0

    def test_add_director_invalid_form(self, client):
        # Arrange
        url = reverse("add_director")
        data = {"name": "", "description": "", "image": "test_image.jpg"}
        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert Director.objects.count() == 0

    def test_add_director_non_unique_name(self, client):
        # Arrange
        Director.objects.create(name="Test Director")
        url = reverse("add_director")
        data = {
            "name": "Test Director",
            "description": "Test Description",
            "image": "test_image.jpg",
        }
        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert Director.objects.count() == 2
