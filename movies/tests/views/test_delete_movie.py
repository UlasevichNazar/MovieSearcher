import pytest

from movies.models import Movie
from movies.views import delete_movie


@pytest.mark.django_db
class TestDeleteMovie:
    def test_delete_movie_success(self, factory, movie):
        request = factory.post(f"/movies/delete/{movie.id}/")
        response = delete_movie(request, movie.id)
        assert response.status_code == 302
        assert response.url == "/movies/"
        assert not Movie.objects.filter(id=movie.id).exists()

    def test_delete_movie_does_not_exist(self, factory):
        request = factory.post("/movies/delete/999/")
        with pytest.raises(Movie.DoesNotExist):
            delete_movie(request, 999)

    def test_delete_movie_not_post(self, factory, movie):
        request = factory.post(f"/movies/delete/{movie.id}/")
        response = delete_movie(request, movie.id)
        assert response.status_code == 302

    def test_delete_movie_success_redirect(self, factory, movie):
        request = factory.post(f"/movies/delete/{movie.id}/")
        response = delete_movie(request, movie.id)
        assert response.status_code == 302
        assert response.url == "/movies/"
        assert not Movie.objects.filter(id=movie.id).exists()
