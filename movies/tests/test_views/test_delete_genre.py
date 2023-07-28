import pytest

from movies.models import Genre
from movies.views import delete_genre


@pytest.mark.django_db
class TestDeleteGenre:
    def test_delete_genre_success(self, factory, genre):
        request = factory.post(f"/delete_genre/{genre.id}/")
        response = delete_genre(request, genre.id)
        assert response.status_code == 302
        assert response.url == "/genres/"
        assert not Genre.objects.filter(id=genre.id).exists()

    def test_delete_genre_does_not_exist(self, factory):
        request = factory.post("/delete_genre/999/")
        with pytest.raises(Genre.DoesNotExist):
            delete_genre(request, 999)

    def test_delete_genre_not_post(self, factory, genre):
        request = factory.post(f"/delete_genre/{genre.id}/")
        response = delete_genre(request, genre.id)
        assert response.status_code == 302

    def test_delete_genre_success_redirect(self, factory, genre):
        request = factory.post(f"/delete_genre/{genre.id}/")
        response = delete_genre(request, genre.id)
        assert response.status_code == 302
        assert response.url == "/genres/"
        assert not Genre.objects.filter(id=genre.id).exists()
