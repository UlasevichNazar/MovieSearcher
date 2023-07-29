import pytest
from django.urls import reverse

from movies.models import Actor


@pytest.mark.django_db
class TestAddActor:
    def test_add_actor_valid_form(self, client):
        # Arrange
        url = reverse("add_actor")
        data = {
            "name": "Test Actor",
            "description": "Test Description",
            "image": "test_image.jpg",
        }
        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert Actor.objects.count() == 1
        assert Actor.objects.filter(name="Test Actor").exists()

    def test_add_actor_empty_form(self, client):
        # Arrange
        url = reverse("add_actor")

        # Act
        response = client.post(url, data={})
        # Assert
        assert response.status_code == 200
        assert Actor.objects.count() == 0

    def test_add_actor_invalid_form(self, client):
        # Arrange
        url = reverse("add_actor")
        data = {"name": "", "description": "", "image": "test_image.jpg"}
        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert Actor.objects.count() == 0

    def test_add_actor_non_unique_name(self, client):
        # Arrange
        Actor.objects.create(name="Test Actor")
        url = reverse("add_actor")
        data = {
            "name": "Test Actor",
            "description": "Test Description",
            "image": "test_image.jpg",
        }
        # Act
        response = client.post(url, data=data)
        # Assert
        assert response.status_code == 200
        assert Actor.objects.count() == 2
