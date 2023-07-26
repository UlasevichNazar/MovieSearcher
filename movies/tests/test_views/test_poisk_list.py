import pytest

from movies.models import Category
from movies.models import Genre
from movies.models import Movie
from movies.views import PoiskList


@pytest.mark.django_db
class TestPoiskList:
    def test_get_genres_returns_all_genres(self, genre):
        # Arrange
        poisk_list = PoiskList()
        expected_genres = list(Genre.objects.all())
        # Act
        actual_genres = list(poisk_list.get_genres())
        # Assert
        assert actual_genres == expected_genres
        assert actual_genres[0] == genre

    def test_get_categories_returns_all_categories(self, category):
        # Arrange
        poisk_list = PoiskList()
        expected_categories = list(Category.objects.all())
        # Act
        actual_categories = list(poisk_list.get_category())
        # Assert
        assert actual_categories == expected_categories
        assert actual_categories[0] == category

    def test_get_years_returns_years_published(self, movie):
        # Arrange
        poisk_list = PoiskList()
        expected_years = list(
            sorted(
                Movie.objects.filter(status=Movie.Status.PUBLISHED)
                .values_list("year", flat=True)
                .distinct()
            )
        )
        # Act
        actual_years = list(poisk_list.get_years())
        # Assert
        assert actual_years == expected_years
        assert actual_years[0] == movie.year

    def test_get_genres_returns_empty_list_if_no_genres(self):
        # Arrange
        poisk_list = PoiskList()
        expected_genres = list(Genre.objects.all())

        # Act
        actual_genres = list(poisk_list.get_genres())

        # Assert
        assert actual_genres == expected_genres

    def test_get_category_returns_empty_list_if_no_categories(self):
        # Arrange
        poisk_list = PoiskList()
        expected_categories = list(Category.objects.all())

        # Act
        actual_categories = list(poisk_list.get_category())

        # Assert
        assert actual_categories == expected_categories

    def test_get_years_returns_empty_list_if_no_published_movies(self):
        # Arrange
        poisk_list = PoiskList()
        expected_years = list(Movie.objects.all())

        # Act
        actual_years = list(poisk_list.get_years())

        # Assert
        assert actual_years == expected_years
