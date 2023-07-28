import pytest
from django.urls import reverse

from movies.models import Genre


@pytest.mark.django_db
class TestCreateGenre:
    def test_create_genre_successfully_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("genre_create")
        data = {
            "name": "Test Genre",
            "description": "Test description",
            "slug": "test-genre",
        }
        response = api_client.post(url, data=data)
        new_genre = Genre.objects.filter(name="Test Genre")
        assert response.status_code == 201
        assert new_genre.exists()
        assert new_genre[0].name == "Test Genre"
        assert new_genre[0].description == "Test description"
        assert new_genre[0].slug == "test-genre"

    def test_create_genre_successfully_by_manager(self, api_client, manager):
        api_client.force_authenticate(manager)
        url = reverse("genre_create")
        data = {
            "name": "Test Genre",
            "description": "Test description",
            "slug": "test-genre",
        }
        response = api_client.post(url, data=data)
        new_genre = Genre.objects.filter(name="Test Genre")
        assert response.status_code == 201
        assert new_genre.exists()
        assert new_genre[0].name == "Test Genre"
        assert new_genre[0].description == "Test description"
        assert new_genre[0].slug == "test-genre"

    def test_create_genre_permission_false(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("genre_create")
        data = {
            "name": "Test Genre",
            "description": "Test description",
            "slug": "test-genre",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_create_genre_with_missing_required_fields(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("category_create")
        data = {
            "description": "Test description",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Genre.objects.filter(description="Test description").exists()
