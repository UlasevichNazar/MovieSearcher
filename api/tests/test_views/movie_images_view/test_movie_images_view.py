import pytest
from django.urls import reverse

from movies.models import Movie_image


@pytest.mark.django_db
class TestMovieImages:
    def test_returns_movie_images_list(self, api_client):
        url = reverse("movie_images_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Movie_image.objects.count()

    def test_returns_correct_serializer_class(self, api_client, movie_image):
        url = reverse("movie_images_list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert list(response.data[0].keys()) == ["id", "name", "image", "movie"]

    def test_allow_any_permissions_classes(self, api_client):
        url = reverse("movie_images_list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_returns_empty_list_when_no_movie_images(self, api_client):
        url = reverse("movie_images_list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_returns_404_error_when_movie_image_not_found(self, api_client):
        response = api_client.get("/movie_image/999/")
        assert response.status_code == 404

    def test_returns_400_error_when_query_parameters(self, api_client):
        response = api_client.get("/api/v1/movie_image/", data={"param": "1"})
        assert response.status_code == 400
        assert response.data["detail"] == "Query parameters are not allowed."
