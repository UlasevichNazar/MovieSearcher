import pytest
from django.urls import reverse

from movies.models import Review


@pytest.mark.django_db
class TestCreateReview:
    def test_create_review_successfully_by_user(self, api_client, user, movie):
        api_client.force_authenticate(user)
        url = reverse("create_reviews")
        data = {"user": user, "text": "Test text for test review", "movie": movie.pk}
        response = api_client.post(url, data=data)

        new_review = Review.objects.filter(user=user)

        assert response.status_code == 201
        assert new_review.exists()
        assert new_review[0].text == "Test text for test review"

    def test_create_review_successfully_by_manager(self, api_client, manager, movie):
        api_client.force_authenticate(manager)
        url = reverse("create_reviews")
        data = {"user": manager, "text": "Test text for test review", "movie": movie.pk}
        response = api_client.post(url, data=data)

        new_review = Review.objects.filter(user=manager)

        assert response.status_code == 201
        assert new_review.exists()
        assert new_review[0].text == "Test text for test review"

    def test_create_review_successfully_by_admin(self, api_client, superuser, movie):
        api_client.force_authenticate(superuser)
        url = reverse("create_reviews")
        data = {
            "user": superuser,
            "text": "Test text for test review",
            "movie": movie.pk,
        }
        response = api_client.post(url, data=data)

        new_review = Review.objects.filter(user=superuser)

        assert response.status_code == 201
        assert new_review.exists()
        assert new_review[0].text == "Test text for test review"

    def test_create_review_by_anonymous_user(self, api_client, movie):
        url = reverse("create_reviews")
        data = {"text": "Test text for test review", "movie": movie.pk}
        response = api_client.post(url, data=data)

        assert response.status_code == 401

    def test_create_review_with_non_exiting_movie(self, api_client, user):
        api_client.force_authenticate(user)
        url = reverse("create_reviews")
        data = {"user": user, "text": "Test text for test review", "movie": 999}
        response = api_client.post(url, data=data)
        assert response.status_code == 400
        assert Review.objects.count() == 0
