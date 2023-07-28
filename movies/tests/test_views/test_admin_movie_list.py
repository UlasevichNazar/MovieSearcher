import pytest

from movies.views import movie_list_admin


@pytest.mark.django_db
class TestMovieListAdmin:
    def test_render_all_movies(self, factory, movie):
        request = factory.get("movies/")
        response = movie_list_admin(request)
        assert response.status_code == 200

    def test_render_filtered_movies(self, factory, movie):
        request = factory.get("/movies/", {"search": "test"})
        response = movie_list_admin(request)
        assert response.status_code == 200

    def test_render_no_movies(self, factory):
        request = factory.get("/movies/")
        response = movie_list_admin(request)
        assert response.status_code == 200

    def test_render_no_movies_found(self, factory, movie):
        request = factory.get("/movies/", {"search": "moviee"})
        response = movie_list_admin(request)
        assert response.status_code == 200
