import pytest
from django.db.utils import DataError
from django.db.utils import IntegrityError

from movies.models import Movie


@pytest.mark.django_db
class TestMovie:
    def test_create_movie_with_all_fields(self, movie, genre, actor, director):
        assert movie.title == "Test Movie"
        assert movie.description == "Test Description"
        assert str(movie.category) == "Test Category"
        assert list(movie.genre.all()) == [genre]
        assert movie.director == director
        assert list(movie.actors.all()) == [actor]
        assert movie.country == "Test Country"
        assert movie.year == 2021
        assert movie.budget == 1000000
        assert movie.fees_in_the_world == 2000000
        assert movie.slug == "test-movie"
        assert movie.status == Movie.Status.PUBLISHED

    def test_create_movie_with_empty_title(self, category, genre, actor, director):
        with pytest.raises(ValueError):
            movie = Movie.objects.create(
                title="",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test Country",
                year=2021,
                budget=1000000,
                fees_in_the_world=2000000,
                slug="test-movie",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_title_longer_than_max_length(
        self, category, genre, actor, director
    ):
        with pytest.raises(DataError):
            movie = Movie.objects.create(
                title="a" * 256,
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test Country",
                year=2021,
                budget=1000000,
                fees_in_the_world=2000000,
                slug="test-movie",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_country_name_longer_than_max_length(
        self, category, genre, actor, director
    ):
        with pytest.raises(DataError):
            movie = Movie.objects.create(
                title="Test Movie",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="C" * 61,
                year=2021,
                budget=1000000,
                fees_in_the_world=2000000,
                slug="test-movie",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_budget_less_than_0(
        self, category, genre, actor, director
    ):
        with pytest.raises(IntegrityError):
            movie = Movie.objects.create(
                title="Test Movie",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test country",
                year=2021,
                budget=-1100,
                fees_in_the_world=2000000,
                slug="test-movie",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_fees_in_the_world_less_than_0(
        self, category, genre, actor, director
    ):
        with pytest.raises(IntegrityError):
            movie = Movie.objects.create(
                title="Test Movie",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test country",
                year=2021,
                budget=1100,
                fees_in_the_world=-2000000,
                slug="test-movie",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_slug_longer_than_max_length(
        self, category, genre, actor, director
    ):
        with pytest.raises(DataError):
            movie = Movie.objects.create(
                title="Test Movie",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test country",
                year=2021,
                budget=1100,
                fees_in_the_world=2000000,
                slug="t" * 101,
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_create_movie_with_empty_slug(self, category, genre, actor, director):
        with pytest.raises(ValueError):
            movie = Movie.objects.create(
                title="Test Movie",
                description="Test Description",
                poster="movie_posters/test_poster.jpg",
                category=category,
                country="Test country",
                year=2021,
                budget=1100,
                fees_in_the_world=2000000,
                slug="",
                status=Movie.Status.PUBLISHED,
            )
            movie.genre.set([genre])
            movie.director = director
            movie.actors.set([actor])
            movie.save()

    def test_update_movie_title(self, movie):
        movie.title = "Updated movie title"
        movie.save()
        assert movie.title == "Updated movie title"

    def test_delete_movie(self, movie):
        movie.delete()
        assert not Movie.objects.filter(title="Test Movie").exists()

    def test_retrieve_movie_invalid_id(self):
        with pytest.raises(Movie.DoesNotExist):
            Movie.objects.get(id=0)
