import pytest

from movies.views import Search


@pytest.mark.django_db
class TestSearch:
    def test_search_query_returns_expected_movies(self, movie, factory):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["movies"]) == 1
        assert response.context_data["movies"][0].title == "Test Movie"

    def test_context_data_contains_expected_movies(self, factory, movie):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["movies"]) == 1
        assert response.context_data["movies"][0].title == "Test Movie"

    def test_context_data_contains_search_query(self, factory):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert response.context_data["s"] == "q=movie&"

    def test_context_data_contains_categories(self, movie, factory, category):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["categories"]) == 1
        assert response.context_data["categories"][0].name == "Test Category"

    def test_context_data_contains_soon_movies(self, factory, movie):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["soon_movies"]) == 0

    def test_context_data_contains_reviews(self, factory, movie, review):
        # Arrange
        request = factory.get("/search/?s=movie")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["reviews"]) == 1
        assert response.context_data["reviews"][0].text == "test review"

    #  Tests that the search query is case-insensitive
    def test_search_query_is_case_insensitive(self, factory, movie):
        # Arrange
        request = factory.get("/search/?s=MOVIE")
        search = Search.as_view()

        # Act
        response = search(request)

        # Assert
        assert len(response.context_data["movies"]) == 1
        assert response.context_data["movies"][0].title == "Test Movie"
