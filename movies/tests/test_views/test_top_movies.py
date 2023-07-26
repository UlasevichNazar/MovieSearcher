import pytest

from movies.models import Category
from movies.models import Movie
from movies.models import Raiting
from movies.views import TopMoviesView


@pytest.mark.django_db
class TestTopMoviesView:
    def test_top_movies_list(self, factory, movie, rating):
        # Arrange
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert len(response.context_data["top_movies"]) > 0

    def test_top_movies_template(self, factory):
        # Arrange
        request = factory.get("/top-movies/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert response.template_name[0] == "movies/top_movies.html"

    def test_top_movies_pagination(self, factory, movie, review):
        # Arrange
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert len(response.context_data["top_movies"]) == 0

    def test_top_movies_context_data(self, factory, movie, review, category):
        # Arrange
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert "categories" in response.context_data
        assert "title" in response.context_data
        assert "soon_movies" in response.context_data
        assert "reviews" in response.context_data

    def test_top_movies_no_published_movies(self, factory):
        # Arrange
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert len(response.context_data["top_movies"]) == 0

    def test_top_movies_no_ratings(self, factory, user, movie):
        # Arrange
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert len(response.context_data["top_movies"]) == 0

    def test_top_movies_published_movies_only(self, factory, user, movie):
        # Arrange
        movie1 = Movie.objects.create(
            title="Test Movie 2",
            description="Test Description 2",
            poster="movie_posters/test2.jpg",
            category=Category.objects.create(
                name="Test Category 2", url="test-category-2"
            ),
            country="Test Country 2",
            year=2021,
            budget=1000000,
            fees_in_the_world=2000000,
            slug="test-movie-2",
            status=Movie.Status.PUBLISHED,
        )
        Raiting.objects.create(movie=movie1, user=user, rating=5)
        request = factory.get("/top/")
        view = TopMoviesView.as_view()

        # Act
        response = view(request)

        # Assert
        assert response.status_code == 200
        assert len(response.context_data["top_movies"]) == 1
