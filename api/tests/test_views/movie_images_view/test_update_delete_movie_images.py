import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from movies.models import Movie_image


@pytest.mark.django_db
class TestUpdateDeleteMovieImage:
    def test_update_movie_image_successfully_by_admin(
        self, api_client, superuser, movie, movie_image
    ):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "movie": movie.pk,
            }
        response = api_client.put(url, data=data)

        updating_movie_image = Movie_image.objects.filter(
            name="Updating Test image for movie #1"
        )

        assert response.status_code == 200
        assert updating_movie_image.exists()
        assert updating_movie_image[0].name == "Updating Test image for movie #1"
        assert updating_movie_image[0].movie.title == "Test Movie"

    def test_update_movie_image_successfully_by_manager(
        self, api_client, manager, movie, movie_image
    ):
        api_client.force_authenticate(manager)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "movie": movie.pk,
            }
        response = api_client.put(url, data=data)

        updating_movie_image = Movie_image.objects.filter(
            name="Updating Test image for movie #1"
        )

        assert response.status_code == 200
        assert updating_movie_image.exists()
        assert updating_movie_image[0].name == "Updating Test image for movie #1"
        assert updating_movie_image[0].movie.title == "Test Movie"

    def test_update_movie_image_permission_false(
        self, api_client, user, movie_image, movie
    ):
        api_client.force_authenticate(user)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "movie": movie.pk,
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_update_non_exiting_movie_image(
        self, api_client, superuser, movie_image, movie
    ):
        api_client.force_authenticate(superuser)
        url = "/api/v1/movie_image/admin/999/"
        image_path = "/app/media/test_updating_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Updating Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_updating_image.png",
                    image_file.read(),
                    content_type="image/jpeg",
                ),
                "movie": movie.pk,
            }
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    def test_delete_movie_image_successfully_by_admin(
        self, superuser, api_client, movie_image
    ):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Movie_image.objects.filter(name="Test movie image").exists()

    def test_delete_movie_image_successfully_by_manager(
        self, manager, api_client, movie_image
    ):
        api_client.force_authenticate(manager)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Movie_image.objects.filter(name="Test movie image").exists()

    def test_delete_movie_image_permissions_false(self, user, api_client, movie_image):
        api_client.force_authenticate(user)
        url = f"/api/v1/movie_image/admin/{movie_image.pk}"
        response = api_client.delete(url)

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_non_exiting_movie_image(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url = "/api/v1/movie_image/admin/999"
        response = api_client.delete(url)
        assert response.status_code == 404
