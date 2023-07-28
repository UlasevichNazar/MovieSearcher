import pytest

from movies.models import Director
from movies.views import edit_director


@pytest.mark.django_db
class TestEditDirector:
    def test_valid_form_submission(self, factory, director):
        # Arrange
        data = {
            "name": "Updated Director",
            "description": "Test Description",
            "image": "",
        }
        request = factory.post("/", data=data)
        # Act
        response = edit_director(request, director.id)
        # Assert
        assert response.status_code == 302
        assert Director.objects.get(id=director.id).name == "Updated Director"

    def test_empty_form_display(self, factory, director):
        # Arrange
        request = factory.get("/")
        # Act
        response = edit_director(request, director.id)
        # Assert
        assert response.status_code == 200

    def test_director_does_not_exist(self, factory):
        # Arrange
        request = factory.get("/")
        # Act
        with pytest.raises(Director.DoesNotExist):
            edit_director(request, 1)

    def test_invalid_form_submission(self, factory, director):
        # Arrange
        data = {"name": "", "description": "Test Description", "image": ""}
        request = factory.post("/", data=data)
        # Act
        response = edit_director(request, director.id)
        # Assert
        assert response.status_code == 200
        assert Director.objects.get(id=director.id).name == "Test"
