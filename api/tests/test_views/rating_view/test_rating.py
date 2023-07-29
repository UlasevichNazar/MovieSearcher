import json

import pytest
from rest_framework.test import force_authenticate

from api.views.rating_view import RatingView
from movies.models import Raiting


@pytest.mark.django_db
class TestRating:
    def test_create_rating_valid_data(self, user, movie, factory):
        data = {"user": user, "movie": movie.pk, "rating": 8}
        request = factory.post("/api/v1/rating/", data=data)
        force_authenticate(request, user=user)
        response = RatingView.as_view({"post": "create"})(request)

        assert response.status_code == 201
        assert Raiting.objects.count() == 1

    def test_update_rating_valid_data(self, user, movie, factory):
        Raiting.objects.create(
            user=user,
            movie=movie,
            rating=5,
        )
        data = {"movie": movie.pk, "rating": 8}
        request = factory.patch(
            "/api/v1/rating/", data=json.dumps(data), content_type="application/json"
        )
        force_authenticate(request, user=user)
        response = RatingView.as_view({"patch": "change_rating"})(request)

        assert response.status_code == 200
        assert Raiting.objects.get(user=user).rating == 8

    def test_create_invalid_rating(self, user, movie, factory):
        data = {"user": user, "movie": movie.pk, "rating": 11}
        request = factory.post("/api/v1/rating/", data=data)
        force_authenticate(request, user=user)
        response = RatingView.as_view({"post": "create"})(request)
        assert response.status_code == 400
        assert Raiting.objects.count() == 0

    def test_create_rating_does_not_exist(self, factory, user):
        data = {"user": user, "movie": 1, "rating": 11}
        request = factory.post("/api/v1/rating/", data=data)
        force_authenticate(request, user=user)
        response = RatingView.as_view({"post": "create"})(request)
        assert response.status_code == 400
