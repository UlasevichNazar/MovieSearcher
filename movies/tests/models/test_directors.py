import pytest
from django.db.utils import DataError

from movies.models import Director


@pytest.mark.django_db
class TestDirector:
    def test_create_director_with_valid_data(self, director):
        assert director.name == "Test"
        assert director.description == "test description"
        assert director.image == "test_image.jpg"

    def test_save_director_with_valid_data(self, director):
        director.save()
        assert Director.objects.count() == 1

    def test_retrieve_director(self, director):
        director.save()
        retrieved_director = Director.objects.get(id=director.id)
        assert retrieved_director == director

    def test_create_director_with_name_longer_than_max_length(self):
        with pytest.raises(DataError):
            Director.objects.create(
                name="d" * 101, description="Test", image="test_image.jpg"
            )

    def test_create_and_save_director_without_name(self):
        with pytest.raises(ValueError):
            director = Director.objects.create(
                description="test", image="test_image.jpg"
            )
            director.save()

    def test_retrieve_director_invalid_id(self):
        with pytest.raises(Director.DoesNotExist):
            Director.objects.get(id=0)
