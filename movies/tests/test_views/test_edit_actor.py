import pytest

from movies.models import Actor
from movies.views import edit_actor


@pytest.mark.django_db
class TestEditActor:
    def test_valid_form_submission(self, factory, actor):
        # Arrange
        data = {"name": "Updated Actor", "description": "Test Description", "image": ""}
        request = factory.post("/", data=data)
        # Act
        response = edit_actor(request, actor.id)
        # Assert
        assert response.status_code == 302
        assert Actor.objects.get(id=actor.id).name == "Updated Actor"

    def test_empty_form_display(self, factory, actor):
        # Arrange
        request = factory.get("/")
        # Act
        response = edit_actor(request, actor.id)
        # Assert
        assert response.status_code == 200

    def test_actor_does_not_exist(self, factory):
        # Arrange
        request = factory.get("/")
        # Act
        with pytest.raises(Actor.DoesNotExist):
            edit_actor(request, 1)

    def test_invalid_form_submission(self, factory, actor):
        # Arrange
        data = {"name": "", "description": "Test Description", "image": ""}
        request = factory.post("/", data=data)
        # Act
        response = edit_actor(request, actor.id)
        # Assert
        assert response.status_code == 200
        assert Actor.objects.get(id=actor.id).name == "Test Actor"
