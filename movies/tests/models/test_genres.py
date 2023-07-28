import pytest
from django.db.utils import DataError
from django.db.utils import IntegrityError

from movies.models import Genre


@pytest.mark.django_db
class TestGenre:
    def test_create_genre_with_valid_value(self, genre):
        assert genre.name == "Test Genre"
        assert genre.description == "Test description"
        assert genre.slug == "test-genre"

    def test_save_genre_with_valid_data(self, genre):
        genre.save()
        assert Genre.objects.count() == 1

    def test_retrieve_genre(self, genre):
        genre.save()
        retrieved_genre = Genre.objects.get(id=genre.id)
        assert retrieved_genre == genre

    def test_create_genres_with_same_slugs(self, genre):
        genre.save()
        with pytest.raises(IntegrityError):
            genre_with_the_same_slug = Genre.objects.create(
                name="Test Genre 2", description="test description", slug="test-genre"
            )
            genre_with_the_same_slug.save()

    def test_create_genre_with_name_longer_than_max_length(self):
        with pytest.raises(DataError):
            Genre.objects.create(name="a" * 101, description="Test", slug="test-genre")

    def test_create_category_with_slug_longer_than_max_length(self):
        with pytest.raises(DataError):
            Genre.objects.create(name="test", description="Test", slug="a" * 161)

    def test_create_genre_with_empty_name(self):
        with pytest.raises(ValueError):
            Genre.objects.create(name="", description="test", slug="test-genre")

    def test_create_genre_with_empty_url(self):
        with pytest.raises(ValueError):
            Genre.objects.create(name="test", description="test", slug="")

    def test_retrieve_genre_invalid_id(self):
        with pytest.raises(Genre.DoesNotExist):
            Genre.objects.get(id=0)
