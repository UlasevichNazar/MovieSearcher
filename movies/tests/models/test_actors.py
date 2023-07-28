import pytest
from django.db.utils import DataError

from movies.models import Actor


@pytest.mark.django_db
class TestActor:
    def test_create_actor_with_valid_data(self, actor):
        assert actor.name == "Test Actor"
        assert actor.description == "test description"
        assert actor.image == "test_actor_image.jpg"

    def test_save_actor_with_valid_data(self, actor):
        actor.save()
        assert Actor.objects.count() == 1

    def test_retrieve_actor(self, actor):
        actor.save()
        retrieved_actor = Actor.objects.get(id=actor.id)
        assert retrieved_actor == actor

    def test_create_actor_with_name_longer_than_max_length(self):
        with pytest.raises(DataError):
            Actor.objects.create(
                name="a" * 101, description="Test", image="test_actor_image.jpg"
            )

    def test_create_and_save_actor_without_name(self):
        with pytest.raises(ValueError):
            actor = Actor.objects.create(description="test", image="test_image.jpg")
            actor.save()

    def test_retrieve_actor_invalid_id(self):
        with pytest.raises(Actor.DoesNotExist):
            Actor.objects.get(id=0)
