import pytest
from django.urls import reverse

from movies.models import Review


@pytest.mark.django_db
class TestReviewList:
    def test_returns_review_list(self, api_client):
        url = reverse("reviews")
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == Review.objects.count()

    def test_returns_correct_serializer_class(self, api_client, review):
        url = reverse("reviews")
        response = api_client.get(url)
        assert response.status_code == 200
        assert list(response.data[0].keys()) == [
            "user",
            "text",
            "created",
            "movie",
        ]

    def test_allow_any_permissions_classes(self, api_client):
        url = reverse("reviews")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_returns_empty_list_when_no_reviews(self, api_client):
        url = reverse("reviews")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_returns_404_error_when_reviews_not_found(self, api_client):
        response = api_client.get("/reviews/999/")
        assert response.status_code == 404
