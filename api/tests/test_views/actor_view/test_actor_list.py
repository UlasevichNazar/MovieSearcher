import pytest
from django.urls import reverse

from movies.models import Actor


@pytest.mark.django_db
class TestActorList:
    def test_returns_actor_list(self, client):
        url = reverse("actors_list")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Actor.objects.count()

    def test_returns_correct_serializer_class(self, client, actor):
        url = reverse("actors_list")
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.data[0].keys()) == ["name", "description", "image"]

    def test_allow_any_permissions_classes(self, client):
        url = reverse("actors_list")
        response = client.get(url)
        assert response.status_code == 200

    def test_returns_empty_list_when_no_actors(self, client):
        url = reverse("actors_list")
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_returns_404_error_when_actor_not_found(self, client):
        response = client.get("/actors/999/")
        assert response.status_code == 404

    def test_returns_400_error_when_query_parameters(self, client):
        response = client.get("/api/v1/actors/", data={"param": "1"})
        assert response.status_code == 400
        assert response.data["detail"] == "Query parameters are not allowed."
