import pytest


@pytest.mark.django_db
class TestRetrieveDirector:
    def test_retrieve_director_by_pk(self, api_client, director):
        url = f"/api/v1/director/{director.pk}/"
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == "Test"
        assert response.data["description"] == "test description"

    def test_director_with_wrong_pk_does_not_exist(self, api_client):
        url = "/api/v1/director/999/"
        response = api_client.get(url)
        assert response.status_code == 404
        assert response.data["detail"] == "Страница не найдена."

    def test_invalid_pk_format(self, api_client):
        url = "/api/v1/director/invalid_pk/"
        response = api_client.get(url)
        assert response.status_code == 404
