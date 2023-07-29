import pytest

from movies.models import Genre
from movies.views import genre_list


@pytest.mark.django_db
class TestGenreList:
    def test_render_all_genres(self, factory, genre):
        Genre.objects.create(name="Serial", slug="serial")
        request = factory.get("genre_list/")
        response = genre_list(request)
        assert response.status_code == 200
        assert "Serial" in str(response.content)
        assert "Test Genre" in str(response.content)

    def test_render_filtered_genres(self, factory, genre):
        Genre.objects.create(name="Serial", slug="serial")
        request = factory.get("/genre_list/", {"search": "ser"})
        response = genre_list(request)
        assert response.status_code == 200
        assert "Serial" in str(response.content)
        assert "Test Category" not in str(response.content)

    def test_render_no_genres(self, factory):
        request = factory.get("/genre_list/")
        response = genre_list(request)
        assert response.status_code == 200

    def test_render_no_genres_found(self, factory, genre):
        Genre.objects.create(name="Serial", slug="serial")
        request = factory.get("/genre_list/", {"search": "mult"})
        response = genre_list(request)
        assert response.status_code == 200
