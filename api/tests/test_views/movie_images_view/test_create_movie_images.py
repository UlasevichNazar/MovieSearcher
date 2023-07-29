import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from movies.models import Movie_image


@pytest.mark.django_db
class TestCreateMovieImages:
    def test_create_movie_image_successfully_by_admin(
        self, api_client, superuser, movie
    ):
        api_client.force_authenticate(superuser)
        url = reverse("movie_images_create")
        image_path = "/app/media/test_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "movie": movie.pk,
            }
        response = api_client.post(url, data=data)
        new_movie_image = Movie_image.objects.filter(name="Test image for movie #1")
        assert response.status_code == 201
        assert new_movie_image.exists()
        assert (
            movie.movie_images.get(name="Test image for movie #1").name
            == new_movie_image[0].name
        )

        new_movie_image[0].delete()

    def test_create_movie_image_successfully_by_manager(
        self, api_client, manager, movie
    ):
        api_client.force_authenticate(manager)
        url = reverse("movie_images_create")
        image_path = "/app/media/test_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "movie": movie.pk,
            }
        response = api_client.post(url, data=data)
        new_movie_image = Movie_image.objects.filter(name="Test image for movie #1")
        assert response.status_code == 201
        assert new_movie_image.exists()
        assert (
            movie.movie_images.get(name="Test image for movie #1").name
            == new_movie_image[0].name
        )

    def test_create_movie_image_permission_false(self, api_client, user, movie):
        api_client.force_authenticate(user)
        url = reverse("movie_images_create")
        image_path = "/app/media/test_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "Test image for movie #1",
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "movie": movie.pk,
            }
        response = api_client.post(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_create_movie_image_with_missing_required_fields(
        self, api_client, superuser
    ):
        api_client.force_authenticate(superuser)
        url = reverse("movie_images_create")
        data = {"name": "Test name"}

        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Movie_image.objects.filter(name="Test name").exists()

    def test_create_movie_image_with_invalid_name(self, api_client, superuser, movie):
        api_client.force_authenticate(superuser)
        url = reverse("movie_images_create")
        image_path = "/app/media/test_image.png"
        with open(image_path, "rb") as image_file:
            data = {
                "name": "T" * 101,
                "image": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "movie": movie.pk,
            }
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert Movie_image.objects.count() == 0
