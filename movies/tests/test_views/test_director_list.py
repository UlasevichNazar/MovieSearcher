import pytest

from movies.models import Director
from movies.views import director_list


@pytest.mark.django_db
class TestDirectorList:
    def test_render_all_directors(self, factory, director):
        Director.objects.create(name="name", image="test__image.jpg")
        request = factory.get("director_list/")
        response = director_list(request)
        assert response.status_code == 200
        assert "name" in str(response.content)
        assert "Test" in str(response.content)

    def test_render_filtered_directors(self, factory, director):
        Director.objects.create(name="name", image="test__image.jpg")
        request = factory.get("/director_list/", {"search": "name"})
        response = director_list(request)
        assert response.status_code == 200
        assert "name" in str(response.content)
        assert "Test" not in str(response.content)

    def test_render_no_directors(self, factory):
        request = factory.get("/director_list/")
        response = director_list(request)
        assert response.status_code == 200

    def test_render_no_directors_found(self, factory, director):
        Director.objects.create(name="name", image="test__image.jpg")
        request = factory.get("/director_list/", {"search": "directoor"})
        response = director_list(request)
        assert response.status_code == 200
