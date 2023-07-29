import pytest

from movies.models import Actor
from movies.views import actor_list


@pytest.mark.django_db
class TestActorList:
    def test_render_all_actors(self, factory, actor):
        Actor.objects.create(name="name", image="test__image.jpg")
        request = factory.get("actor_list/")
        response = actor_list(request)
        assert response.status_code == 200
        assert "name" in str(response.content)
        assert "Test Actor" in str(response.content)

    def test_render_filtered_actors(self, factory, actor):
        Actor.objects.create(name="name", image="test__image.jpg")
        request = factory.get("/actor_list/", {"search": "name"})
        response = actor_list(request)
        assert response.status_code == 200
        assert "name" in str(response.content)
        assert "Test Actor" not in str(response.content)

    def test_render_no_actors(self, factory):
        request = factory.get("/actor_list/")
        response = actor_list(request)
        assert response.status_code == 200

    def test_render_no_actors_found(self, factory, actor):
        Actor.objects.create(name="name", image="test__image.jpg")
        request = factory.get("/actor_list/", {"search": "actooor"})
        response = actor_list(request)
        assert response.status_code == 200
