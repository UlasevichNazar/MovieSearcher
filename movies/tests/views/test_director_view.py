import pytest
from django.http import Http404

from movies.models import Category
from movies.models import Director
from movies.models import Movie
from movies.models import Review
from movies.views import DirectorView


@pytest.mark.django_db
class TestActorView:
    def test_director_details_displayed_correctly(self, factory, director):
        # Arrange
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act
        response = view(request, slug=f"{director.name}")

        # Assert
        assert response.status_code == 200
        assert response.template_name[0] == "persons/directors.html"

    def test_all_categories_displayed(self, factory, category, director):
        # Arrange
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act
        response = view(request, slug=f"{director.name}")

        # Assert
        assert response.status_code == 200
        assert Category.objects.count() == len(response.context_data["categories"])

    def test_all_soon_movies_displayed(self, factory, director):
        # Arrange
        Movie.objects.create(
            title="Test Movie", slug="test-movie", status=Movie.Status.DRAFT
        )
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act
        response = view(request, slug=f"{director.name}")

        # Assert
        assert response.status_code == 200
        assert Movie.objects.filter(status=Movie.Status.DRAFT).count() == len(
            response.context_data["soon_movies"]
        )

    def test_all_reviews_displayed(self, factory, movie, user, review, director):
        # Arrange
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act
        response = view(request, slug=f"{director.name}")

        # Assert
        assert response.status_code == 200
        assert Review.objects.count() == len(response.context_data["reviews"])

    def test_director_with_empty_name_raises_value_error(self):
        # Arrange
        director = Director(image="test.jpg")

        # Assert
        with pytest.raises(ValueError):
            director.save()

    def test_director_not_found_returns_404_error(self, factory, director):
        # Arrange
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act & Assert
        with pytest.raises(Http404):
            view(request, slug="test-director")

    def test_director_with_no_image_displayed_correctly(self, factory):
        # Arrange
        director = Director.objects.create(name="Test Director")
        request = factory.get("/director/")
        view = DirectorView.as_view()

        # Act
        response = view(request, slug=f"{director.name}")

        # Assert
        assert response.status_code == 200
