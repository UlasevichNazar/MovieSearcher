import pytest
from django.urls import reverse

from movies.forms import GenreForm
from movies.models import Genre
from movies.views import add_genre


@pytest.mark.django_db
class TestAddGenre:
    def test_valid_form(self, client):
        # Arrange
        url = reverse("add_genre")
        data = {
            "name": "Test Genre",
            "slug": "test-genre",
            "description": "This is a test genre.",
        }
        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert Genre.objects.count() == 1
        assert Genre.objects.filter(name="Test Genre").exists()

    def test_invalid_form(self, factory):
        # Arrange
        request = factory.post("/add/genre/")
        form_data = {"name": "", "slug": "", "description": ""}
        GenreForm(data=form_data)

        # Act
        response = add_genre(request)

        # Assert
        assert response.status_code == 200
        assert not Genre.objects.filter(name="").exists()

    def test_empty_fields(self, factory):
        # Arrange
        factory.post("/add/genre/")
        form_data = {"name": "", "slug": "", "description": ""}
        form = GenreForm(data=form_data)

        # Act & Assert
        with pytest.raises(ValueError):
            form.save()

    #  Tests that the page displays correct form layout
    def test_form_layout(self, factory):
        # Arrange
        request = factory.get("/add/genre/")

        # Act
        response = add_genre(request)

        # Assert
        assert response.status_code == 200
