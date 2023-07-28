import pytest

from movies.forms import GenreForm
from movies.models import Genre
from movies.views import edit_genre


@pytest.mark.django_db
class TestEditGenre:
    def test_valid_form_save(self, genre):
        # Given
        data = {
            "name": "Updated Genre",
            "slug": "updated-genre",
            "description": "Test description",
        }
        form = GenreForm(data=data, instance=genre)

        # When
        form.is_valid()
        form.save()
        updated_genre = Genre.objects.get(id=genre.id)

        # Then
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.slug == "updated-genre"
        assert updated_genre.description == "Test description"

    #  Tests that a valid form updates data in the database
    def test_valid_form_update(self, genre):
        # Given
        data = {
            "name": "Updated Genre",
            "slug": "updated-genre",
            "description": "Test description",
        }
        form = GenreForm(data=data, instance=genre)

        # When
        form.is_valid()
        form.save()
        updated_genre = Genre.objects.get(id=genre.id)

        data = {
            "name": "New Name",
            "slug": "new-slug",
            "description": "New description",
        }
        form = GenreForm(data=data, instance=updated_genre)

        form.is_valid()
        form.save()
        updated_genre.refresh_from_db()

        # Then
        assert updated_genre.name == "New Name"
        assert updated_genre.slug == "new-slug"
        assert updated_genre.description == "New description"

    #  Tests that an error is raised if the genre does not exist
    def test_genre_does_not_exist(self):
        # Given
        genre_id = 1

        # When
        with pytest.raises(Genre.DoesNotExist):
            edit_genre(None, genre_id)

        # Then
        assert True

    #  Tests that an error is raised if the form is invalid
    def test_invalid_form(self):
        # Given
        genre = Genre.objects.create(name="Test Genre", slug="test-genre")
        data = {"name": "", "slug": "", "description": "Test description"}
        form = GenreForm(data=data, instance=genre)

        # When
        is_valid = form.is_valid()

        # Then
        assert not is_valid
