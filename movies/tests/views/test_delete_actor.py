import pytest

from movies.models import Actor
from movies.views import delete_actor


@pytest.mark.django_db
class TestDeleteActor:
    def test_delete_actor_success(self, factory, actor):
        request = factory.post(f"/delete_actor/{actor.id}/")
        response = delete_actor(request, actor.id)
        assert response.status_code == 302
        assert response.url == "/actors/"
        assert not Actor.objects.filter(id=actor.id).exists()

    def test_delete_actor_does_not_exist(self, factory):
        request = factory.post("/delete_actor/999/")
        with pytest.raises(Actor.DoesNotExist):
            delete_actor(request, 999)

    def test_delete_actor_not_post(self, factory, actor):
        request = factory.post(f"/delete_actor/{actor.id}/")
        response = delete_actor(request, actor.id)
        assert response.status_code == 302

    def test_delete_actor_success_redirect(self, factory, actor):
        request = factory.post(f"/delete_actor/{actor.id}/")
        response = delete_actor(request, actor.id)
        assert response.status_code == 302
        assert response.url == "/actors/"
        assert not Actor.objects.filter(id=actor.id).exists()
