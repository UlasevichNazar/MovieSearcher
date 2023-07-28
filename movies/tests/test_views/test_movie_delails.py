import pytest
from django.http import Http404

from movies.models import Raiting
from movies.views import MovieDetail


@pytest.mark.django_db
class TestMovieDetail:
    def test_movie_detail_page_loads_successfully(self, factory, movie, user):
        # Arrange
        request = factory.get("/movie-detail/")
        request.user = user
        view = MovieDetail.as_view()

        # Act
        response = view(request, slug=movie.slug)

        # Assert
        assert response.status_code == 200
        assert response.template_name[0] == "movies/movie_detail.html"

    def test_average_rating_and_rating_count_are_displayed(
        self, factory, movie, user, rating
    ):
        # Arrange
        request = factory.get("/movie-detail/")
        request.user = user
        view = MovieDetail.as_view()

        # Act
        response = view(request, slug=movie.slug)

        # Assert
        assert response.status_code == 200
        assert response.context_data["average_rating"] == 5.0
        assert response.context_data["rating_count"] == 1

    def test_user_can_rate_a_movie(self, factory, movie, user):
        # Arrange
        request = factory.post("/movie-detail/")
        request.user = user
        request.POST = {"rating": 5}
        view = MovieDetail.as_view()

        # Act
        response = view(request, slug=movie.slug)

        # Assert
        assert response.status_code == 302
        assert Raiting.objects.filter(user=user, movie=movie).exists()

    def test_user_can_delete_their_rating(self, factory, movie, user, rating):
        # Arrange
        request = factory.post("/movie-detail/")

        request.user = user
        view = MovieDetail.as_view()

        # Act
        response = view(request, slug=movie.slug)

        # Assert
        assert response.status_code == 302
        assert not Raiting.objects.filter(user=user, movie=movie).exists()

    def test_movie_does_not_exist(self, factory):
        # Arrange
        request = factory.get("/movie-detail/")
        view = MovieDetail.as_view()

        # Act & Assert
        with pytest.raises(Http404):
            view(request, slug="non-existent-movie")
