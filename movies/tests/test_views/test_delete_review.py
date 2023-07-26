import pytest
from django.http import Http404
from django.urls import reverse

from movies.models import Review
from movies.views import delete_review
from user.admin import User


@pytest.mark.django_db
class TestDeleteReview:
    def test_delete_review_successfully_as_review_creator(
        self, factory, user, movie, review
    ):
        # Arrange
        url = movie.get_absolute_url()
        request = factory.post(url)
        request.user = user
        # Act
        response = delete_review(request, review.pk)
        # Assert
        assert response.status_code == 302
        assert response.url == url
        assert not Review.objects.filter(pk=review.pk).exists()

    def test_delete_review_successfully_as_superuser(self, movie, factory):
        # Arrange
        superuser = User.objects.create_superuser(
            username="testuser", email="test@test.com", password="12345"
        )
        review = Review.objects.create(user=superuser, text="Test review", movie=movie)
        url = movie.get_absolute_url()
        request = factory.post(url)
        request.user = superuser
        # Act
        response = delete_review(request, review.pk)
        # Assert
        assert response.status_code == 302
        assert response.url == url
        assert not Review.objects.filter(pk=review.pk).exists()

    def test_delete_review_successfully_as_staff_user(self, factory, movie):
        # Arrange
        manager = User.objects.create_user(
            username="testuser", email="test@test.com", password="12345", is_staff=True
        )
        review = Review.objects.create(user=manager, text="Test review", movie=movie)
        url = movie.get_absolute_url()
        request = factory.post(url)
        request.user = manager
        # Act
        response = delete_review(request, review.pk)
        # Assert
        assert response.status_code == 302
        assert response.url == url
        assert not Review.objects.filter(pk=review.pk).exists()

    def test_delete_review_returns_404_error_when_review_does_not_exist(
        self, factory, movie, user
    ):
        # Arrange
        url = reverse("delete_review", args=[1])
        request = factory.post(url)
        request.user = user
        # Act
        with pytest.raises(Http404):
            delete_review(request, 1)
