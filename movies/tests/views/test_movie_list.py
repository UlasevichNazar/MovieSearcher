import pytest
from django.http import Http404

from movies.models import Category
from movies.models import Movie
from movies.models import Review
from movies.views import MovieList


@pytest.mark.django_db
class TestMovieList:
    def test_response_status_code(self, factory):
        request = factory.get("/")
        response = MovieList.as_view()(request)
        assert response.status_code == 200

    def test_correct_template(self, factory):
        request = factory.get("/")
        response = MovieList.as_view()(request)
        assert "movies/movie_list.html" in response.template_name

    def test_correct_context_data(self, factory, category, review):
        request = factory.get("/")
        response = MovieList.as_view()(request)
        assert response.context_data["categories"].count() == 1
        assert (
            response.context_data["categories"].count()
            == Category.objects.all().count()
        )
        assert response.context_data["title"] == "Главная страница"
        assert (
            response.context_data["soon_movies"].count()
            == Movie.objects.filter(status=Movie.Status.DRAFT).count()
        )
        assert response.context_data["reviews"].count() == Review.objects.all().count()
        assert response.context_data["reviews"].count() == 1

    def test_correct_number_of_paginated_objects(self, factory, movie):
        request = factory.get("/")
        response = MovieList.as_view()(request)
        assert len(response.context_data["movies"]) == 1

    def test_only_published_movies(self, factory, movie):
        request = factory.get("/")
        response = MovieList.as_view()(request)
        for movie in response.context_data["movies"]:
            assert movie.status == Movie.Status.PUBLISHED

    def test_no_movies_out_of_range(self, factory):
        request = factory.get("/?page=100")
        with pytest.raises(Http404):
            MovieList.as_view()(request)

    def test_no_movies_not_integer(self, rf):
        request = rf.get("/?page=abc")
        with pytest.raises(Http404):
            MovieList.as_view()(request)
