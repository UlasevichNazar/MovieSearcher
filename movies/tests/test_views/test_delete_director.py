import pytest

from movies.models import Director
from movies.views import delete_director


@pytest.mark.django_db
class TestDeleteDirector:
    def test_delete_actor_success(self, factory, director):
        request = factory.post(f"/delete_director/{director.id}/")
        response = delete_director(request, director.id)
        assert response.status_code == 302
        assert response.url == "/directors/"
        assert not Director.objects.filter(id=director.id).exists()

    def test_delete_director_does_not_exist(self, factory):
        request = factory.post("/delete_director/999/")
        with pytest.raises(Director.DoesNotExist):
            delete_director(request, 999)

    def test_delete_director_not_post(self, factory, director):
        request = factory.post(f"/delete_director/{director.id}/")
        response = delete_director(request, director.id)
        assert response.status_code == 302

    def test_delete_actor_success_redirect(self, factory, director):
        request = factory.post(f"/delete_director/{director.id}/")
        response = delete_director(request, director.id)
        assert response.status_code == 302
        assert response.url == "/directors/"
        assert not Director.objects.filter(id=director.id).exists()
