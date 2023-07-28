import pytest
from django.urls import reverse

from movies.models import Director


@pytest.mark.django_db
class TestDirectorList:
    def test_returns_director_list(self, api_client):
        url = reverse("directors_list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Director.objects.count()

    def test_returns_correct_serializer_class(self, api_client, director):
        url = reverse("directors_list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert list(response.data[0].keys()) == ["name", "description", "image"]

    def test_allow_any_permissions_classes(self, api_client):
        url = reverse("directors_list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_returns_empty_list_when_no_directors(self, api_client):
        url = reverse("directors_list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_returns_404_error_when_director_not_found(self, api_client):
        response = api_client.get("/directors/999/")
        assert response.status_code == 404

    def test_returns_400_error_when_query_parameters(self, api_client):
        response = api_client.get("/api/v1/director/", data={"param": "1"})
        assert response.status_code == 400
        assert response.data["detail"] == "Query parameters are not allowed."
