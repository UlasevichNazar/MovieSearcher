import pytest
from django.db.utils import DataError

from movies.models import Movie_image


@pytest.mark.django_db
class TestMovieImages:
    def test_create_movie_images_with_all_fields(self, movie_image, movie):
        assert movie.movie_images.get(name="Test movie image") == movie_image

    def test_retrieve_movie_image(self, movie_image, movie):
        movie_image.save()
        retrieved_movie_image = Movie_image.objects.get(id=movie_image.id)
        assert retrieved_movie_image == movie_image

    def test_create_movie_image_with_name_longer_than_max_length(self, movie):
        with pytest.raises(DataError):
            movie_image = Movie_image.objects.create(
                name="m" * 101, image="movie_image.jpg", movie=movie
            )
            movie_image.save()

    def test_create_movie_image_with_empty_name(self, movie):
        with pytest.raises(ValueError):
            movie_image = Movie_image.objects.create(
                name="", image="movie_image.jpg", movie=movie
            )
            movie_image.save()

    def test_create_movie_image_with_empty_image(self, movie):
        with pytest.raises(ValueError):
            movie_image = Movie_image.objects.create(
                name="test movie image", image="", movie=movie
            )
            movie_image.save()

    def test_retrieve_movie_image_invalid_id(self):
        with pytest.raises(Movie_image.DoesNotExist):
            Movie_image.objects.get(id=0)
