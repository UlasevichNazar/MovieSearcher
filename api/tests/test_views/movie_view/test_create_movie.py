import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
class TestCreateMovie:
    def test_create_movie_successfully_by_admin(
        self, api_client, superuser, category, genre, director, actor
    ):
        url = reverse("movie_create_view")
        api_client.force_authenticate(superuser)
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Test Movie",
                "description": "Test description",
                "poster": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "category": category.pk,
                "actors": (actor.pk,),
                "director": director.pk,
                "genre": (genre.pk,),
                "country": "Test Country",
                "year": 2021,
                "budget": 1000000,
                "fees_in_the_world": 2000000,
                "slug": "test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.post(url, data=data)
        new_movie = Movie.objects.filter(title="Test Movie")
        assert response.status_code == 201
        assert new_movie.exists()

    def test_create_movie_successfully_by_manager(
        self, api_client, manager, category, genre, director, actor
    ):
        url = reverse("movie_create_view")
        api_client.force_authenticate(manager)
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Test Movie",
                "description": "Test description",
                "poster": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "category": category.pk,
                "actors": (actor.pk,),
                "director": director.pk,
                "genre": (genre.pk,),
                "country": "Test Country",
                "year": 2021,
                "budget": 1000000,
                "fees_in_the_world": 2000000,
                "slug": "test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.post(url, data=data)
        new_movie = Movie.objects.filter(title="Test Movie")
        assert response.status_code == 201
        assert new_movie.exists()

    def test_create_movie_permissions_false(
        self, api_client, user, category, genre, director, actor
    ):
        url = reverse("movie_create_view")
        api_client.force_authenticate(user)
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "Test Movie",
                "description": "Test description",
                "poster": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
                "category": category.pk,
                "actors": (actor.pk,),
                "director": director.pk,
                "genre": (genre.pk,),
                "country": "Test Country",
                "year": 2021,
                "budget": 1000000,
                "fees_in_the_world": 2000000,
                "slug": "test-movie",
                "status": Movie.Status.PUBLISHED,
            }
        response = api_client.post(url, data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_create_movie_with_missing_required_fields(self, api_client, superuser):
        url = reverse("movie_create_view")
        api_client.force_authenticate(superuser)
        image_path = "/app/media/test_image.png"

        with open(image_path, "rb") as image_file:
            data = {
                "title": "",
                "description": "Test description",
                "poster": SimpleUploadedFile(
                    "test_image.png", image_file.read(), content_type="image/jpeg"
                ),
            }
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert not Movie.objects.filter(description="Test description").exists()
