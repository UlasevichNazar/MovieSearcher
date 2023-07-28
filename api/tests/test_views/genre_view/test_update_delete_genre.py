import pytest

from movies.models import Genre


@pytest.mark.django_db
class TestUpdateDeleteGenre:
    def test_update_genre_successfully_by_admin(self, api_client, superuser, genre):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        data = {
            "name": "Update Test Genre",
            "description": "Update Test description",
            "slug": "update-test-genre",
        }
        response = api_client.put(url, data=data)
        updating_genre = Genre.objects.filter(name="Update Test Genre")
        assert response.status_code == 200
        assert updating_genre.exists()
        assert updating_genre[0].name == "Update Test Genre"
        assert updating_genre[0].description == "Update Test description"
        assert updating_genre[0].slug == "update-test-genre"

    def test_update_genre_successfully_by_manager(self, api_client, manager, genre):
        api_client.force_authenticate(manager)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        data = {
            "name": "Update Test Genre",
            "description": "Update Test description",
            "slug": "update-test-genre",
        }
        response = api_client.put(url, data=data)
        updating_genre = Genre.objects.filter(name="Update Test Genre")
        assert response.status_code == 200
        assert updating_genre.exists()
        assert updating_genre[0].name == "Update Test Genre"
        assert updating_genre[0].description == "Update Test description"
        assert updating_genre[0].slug == "update-test-genre"

    def test_update_genre_permissions_false(self, api_client, user, genre):
        api_client.force_authenticate(user)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        data = {
            "name": "Update Test Genre",
            "description": "Update Test description",
            "slug": "update-test-genre",
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_update_non_exiting_genre(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/genre/admin/999/"
        data = {
            "name": "Update Test Genre",
            "description": "Update Test description",
            "slug": "update-test-genre",
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_genre_successfully_by_admin(self, api_client, genre, superuser):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Genre.objects.filter(name="Test Genre").exists()

    def test_delete_genre_successfully_by_manager(self, api_client, genre, manager):
        api_client.force_authenticate(manager)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Genre.objects.filter(name="Test Genre").exists()

    def test_delete_genre_permissions_false(self, api_client, genre, user):
        api_client.force_authenticate(user)
        url = f"/api/v1/genre/admin/{genre.pk}/"
        response = api_client.delete(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )
        assert Genre.objects.filter(name="Test Genre").exists()

    def test_delete_non_exiting_genre(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/genre/admin/999/"
        response = api_client.delete(url)
        assert response.status_code == 404
