import pytest
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
class TestMovieList:
    def test_returns_movie_list(self, api_client):
        url = reverse("movie_view")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Movie.objects.count()

    def test_returns_correct_serializer_class_for_users(self, api_client, user, movie):
        api_client.force_authenticate(user)
        url = reverse("movie_view")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_returns_correct_serializer_class_for_staff_and_admin(
        self, api_client, manager, movie
    ):
        api_client.force_authenticate(manager)
        url = reverse("movie_view")
        response = api_client.get(url)
        assert response.status_code == 200
        assert list(response.data[0].keys()) == [
            "id",
            "title",
            "poster",
            "category",
            "publish",
        ]

    def test_returns_empty_list_when_no_movies(self, api_client):
        url = reverse("movie_view")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_returns_404_error_when_movie_not_found(self, api_client):
        response = api_client.get("api/v1/movie/999/")
        assert response.status_code == 404

    def test_returns_400_error_when_query_parameters(self, api_client):
        response = api_client.get("/api/v1/movie/", data={"param": "1"})
        assert response.status_code == 400
        assert response.data["detail"] == "Query parameters are not allowed."
