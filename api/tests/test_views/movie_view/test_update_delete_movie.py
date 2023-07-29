import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
class TestUpdateDeleteMovie:
    def test_update_successfully_movie_by_admin(self, api_client, superuser, movie):
        api_client.force_authenticate(superuser)
        url = reverse("movie_update_destroy_view", kwargs={"slug": movie.slug})
        image_path = "/app/media/test_updating_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Update Test Movie",
                "description": "Update Test description",
                "poster": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "country": "Update Test Country",
                "year": 2023,
                "budget": 1000001,
                "fees_in_the_world": 2000001,
                "slug": "update-test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.put(url, data=data)
        updating_movie = Movie.objects.filter(title="Update Test Movie")

        assert response.status_code == 200
        assert updating_movie.exists()
        assert updating_movie[0].title == "Update Test Movie"
        assert updating_movie[0].description == "Update Test description"
        assert updating_movie[0].country == "Update Test Country"

    def test_update_successfully_movie_by_manager(self, api_client, manager, movie):
        api_client.force_authenticate(manager)
        url = reverse("movie_update_destroy_view", kwargs={"slug": movie.slug})
        image_path = "/app/media/test_updating_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Update Test Movie",
                "description": "Update Test description",
                "poster": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "country": "Update Test Country",
                "year": 2023,
                "budget": 1000001,
                "fees_in_the_world": 2000001,
                "slug": "update-test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.put(url, data=data)
        updating_movie = Movie.objects.filter(title="Update Test Movie")

        assert response.status_code == 200
        assert updating_movie.exists()
        assert updating_movie[0].title == "Update Test Movie"
        assert updating_movie[0].description == "Update Test description"
        assert updating_movie[0].country == "Update Test Country"

    def test_update_movie_permissions_false(self, api_client, user, movie):
        api_client.force_authenticate(user)
        url = reverse("movie_update_destroy_view", kwargs={"slug": movie.slug})
        image_path = "/app/media/test_updating_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Update Test Movie",
                "description": "Update Test description",
                "poster": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "country": "Update Test Country",
                "year": 2023,
                "budget": 1000001,
                "fees_in_the_world": 2000001,
                "slug": "update-test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_update_non_exiting_movie(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("movie_update_destroy_view", kwargs={"slug": "aaaa"})
        image_path = "/app/media/test_updating_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Update Test Movie",
                "description": "Update Test description",
                "poster": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "country": "Update Test Country",
                "year": 2023,
                "budget": 1000001,
                "fees_in_the_world": 2000001,
                "slug": "update-test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_movie_successfully_by_admin(self, api_client, superuser, movie):
        api_client.force_authenticate(superuser)
        url = reverse("movie_update_destroy_view", kwargs={"slug": "test-movie"})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Movie.objects.filter(title="Test Movie").exists()

    def test_delete_movie_successfully_by_manager(self, api_client, manager, movie):
        api_client.force_authenticate(manager)
        url = reverse("movie_update_destroy_view", kwargs={"slug": "test-movie"})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Movie.objects.filter(title="Test Movie").exists()

    def test_delete_movie_permissions_false(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("movie_update_destroy_view", kwargs={"slug": "test-movie"})
        response = api_client.delete(url)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_non_exiting_movie(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = reverse("movie_update_destroy_view", kwargs={"slug": "test"})
        response = api_client.delete(url)
        assert response.status_code == 404
