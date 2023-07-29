import pytest


@pytest.mark.django_db
class TestRetrieveMovie:
    def test_retrieve_movie_by_id(self, api_client, movie):
        url = f"/api/v1/movie/{movie.slug}/"
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == "Test Movie"
        assert response.data["description"] == movie.description

    def test_director_with_wrong_slug_does_not_exist(self, api_client):
        url = "/api/v1/movie/abv/"
        response = api_client.get(url)
        assert response.status_code == 404
        assert response.data["detail"] == "Страница не найдена."

    def test_invalid_pk_format(self, api_client):
        url = "/api/v1/movie/invalid_pk/"
        response = api_client.get(url)
        assert response.status_code == 404
