import pytest


@pytest.mark.django_db
class TestRetrieveActor:
    def test_retrieve_actor_by_pk(self, client, actor):
        url = f"/api/v1/actors/{actor.pk}/"
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == "Test Actor"
        assert response.data["description"] == "test description"

    def test_actor_with_wrong_pk_does_not_exist(self, client):
        url = "/api/v1/actors/999/"
        response = client.get(url)
        assert response.status_code == 404
        assert response.data["detail"] == "Страница не найдена."

    def test_invalid_pk_format(self, client):
        url = "/api/v1/actors/invalid_pk/"
        response = client.get(url)
        assert response.status_code == 404
