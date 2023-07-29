from urllib.parse import urlsplit

import pytest
from django.urls import reverse

from movies.models import Movie
from movies.models import Review


@pytest.mark.django_db
class TestAddReview:
    def test_valid_review_submission(self, movie, user, client):
        # Arrange
        client.force_login(user)
        data = {"text": "Test Review"}
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 302
        assert response.url == reverse("movie_detail", kwargs={"slug": movie.slug})
        assert Review.objects.filter(
            user=user, movie=movie, text="Test Review"
        ).exists()

    def test_user_not_logged_in(self, client, movie):
        # Arrange
        data = {"text": "Test Review"}
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.post(url, data=data, follow=True)

        # Assert
        assert response.status_code == 200
        redirect_path = urlsplit(response.redirect_chain[0][0]).path
        expected_path = reverse("django_login")
        assert redirect_path == expected_path
        assert not Review.objects.filter(movie=movie, text="Test Review").exists()

    def test_invalid_movie_id(self, client, user):
        # Arrange
        client.force_login(user)
        data = {"text": "Test Review"}
        url = reverse("add_review", kwargs={"pk": 1})

        # Act
        with pytest.raises(Movie.DoesNotExist):
            client.post(url, data=data)

        # Assert
        assert not Review.objects.filter(user=user, text="Test Review").exists()

    def test_invalid_review_form_submission(self, client, user, movie):
        # Arrange

        client.force_login(user)
        data = {"text": ""}
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert response.context_data["form"].errors == {"text": ["Обязательное поле."]}
        assert not Review.objects.filter(user=user, movie=movie).exists()

    def test_review_form_invalid_redirect(self, client, user, movie):
        # Arrange
        client.force_login(user)
        data = {"text": ""}
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert response.context_data["form"].errors == {"text": ["Обязательное поле."]}
        assert response.context_data["movie"] == movie
        assert response.context_data["soon_movies"].count() == 0
        assert response.context_data["reviews"].count() == 0

    def test_review_not_saved_invalid_form(self, client, user, movie):
        # Arrange
        client.force_login(user)
        data = {"text": ""}
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.post(url, data=data)

        # Assert
        assert response.status_code == 200
        assert not Review.objects.filter(user=user, movie=movie).exists()

    def test_context_data_includes_movie(self, client, user, movie):
        # Arrange
        client.force_login(user)
        url = reverse("add_review", kwargs={"pk": movie.pk})

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == 200
        assert response.context_data["movie"] == movie
