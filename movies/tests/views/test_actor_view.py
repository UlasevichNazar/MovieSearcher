import pytest
from django.http import Http404

from movies.models import Actor
from movies.models import Category
from movies.models import Movie
from movies.models import Review
from movies.views import ActorView


@pytest.mark.django_db
class TestActorView:
    def test_actor_details_displayed_correctly(self, factory, actor):
        # Arrange
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act
        response = view(request, slug=f"{actor.name}")

        # Assert
        assert response.status_code == 200
        assert response.template_name[0] == "persons/actors.html"

    def test_all_categories_displayed(self, factory, category, actor):
        # Arrange
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act
        response = view(request, slug=f"{actor.name}")

        # Assert
        assert response.status_code == 200
        assert Category.objects.count() == len(response.context_data["categories"])

    def test_all_soon_movies_displayed(self, factory, actor):
        # Arrange
        Movie.objects.create(
            title="Test Movie", slug="test-movie", status=Movie.Status.DRAFT
        )
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act
        response = view(request, slug=f"{actor.name}")

        # Assert
        assert response.status_code == 200
        assert Movie.objects.filter(status=Movie.Status.DRAFT).count() == len(
            response.context_data["soon_movies"]
        )

    def test_all_reviews_displayed(self, factory, movie, user, review, actor):
        # Arrange
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act
        response = view(request, slug=f"{actor.name}")

        # Assert
        assert response.status_code == 200
        assert Review.objects.count() == len(response.context_data["reviews"])

    def test_actor_with_empty_name_raises_value_error(self):
        # Arrange
        actor = Actor(image="test.jpg")

        # Assert
        with pytest.raises(ValueError):
            actor.save()

    def test_actor_not_found_returns_404_error(self, factory, actor):
        # Arrange
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act & Assert
        with pytest.raises(Http404):
            view(request, slug="test-actor")

    def test_actor_with_no_image_displayed_correctly(self, factory):
        # Arrange
        actor = Actor.objects.create(name="Test Actor")
        request = factory.get("/actor/")
        view = ActorView.as_view()

        # Act
        response = view(request, slug=f"{actor.name}")

        # Assert
        assert response.status_code == 200
