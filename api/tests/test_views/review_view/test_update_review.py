import pytest

from movies.models import Review


@pytest.mark.django_db
class TestUpdateReview:
    def test_update_review_successfully_by_owner(self, user, movie, api_client, review):
        api_client.force_authenticate(user)
        url = f"/api/v1/reviews/update/{review.pk}/"
        data = {"text": "Update text"}
        response = api_client.put(url, data=data)
        updating_review = Review.objects.filter(text="Update text")
        assert response.status_code == 200
        assert updating_review.exists()

    def test_update_review_wrong_user(self, api_client, superuser, review):
        api_client.force_authenticate(superuser)
        url = f"/api/v1/reviews/update/{review.pk}/"
        data = {"text": "Update text"}
        response = api_client.put(url, data=data)
        assert response.status_code == 404
        assert response.data["detail"] == "Страница не найдена."

    def test_update_non_exiting_review(self, api_client, user):
        api_client.force_authenticate(user)
        url = "/api/v1/reviews/update/999/"
        data = {"text": "Update text"}
        response = api_client.put(url, data=data)
        assert response.status_code == 404
        assert response.data["detail"] == "Страница не найдена."
