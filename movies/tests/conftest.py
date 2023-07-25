import pytest

from movies.models import Actor
from movies.models import Category
from movies.models import Director
from movies.models import Genre
from movies.models import Movie
from movies.models import Movie_image
from movies.models import Raiting
from movies.models import Review
from user.models import User


@pytest.fixture
def category() -> Category:
    category = Category.objects.create(
        name="Test Category", description="Test description", url="test-category"
    )
    return category


@pytest.fixture
def genre() -> Genre:
    genre = Genre.objects.create(
        name="Test Genre", description="Test description", slug="test-genre"
    )
    return genre


@pytest.fixture
def director() -> Director:
    director = Director.objects.create(
        name="Test", description="test description", image="test_image.jpg"
    )
    return director


@pytest.fixture
def actor() -> Actor:
    actor = Actor.objects.create(
        name="Test Actor", description="test description", image="test_actor_image.jpg"
    )
    return actor


@pytest.fixture
def movie(category, genre, actor, director) -> Movie:
    movie = Movie.objects.create(
        title="Test Movie",
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
    return movie


@pytest.fixture
def movie_image(movie) -> Movie_image:
    movie_image = Movie_image.objects.create(
        name="Test movie image", image="movie_image.jpg", movie=movie
    )
    return movie_image


@pytest.fixture
def user() -> User:
    user = User.objects.create_user(
        username="Test",
        email="test@test.com",
        password="testtest123321",
        free_mailing_list=False,
        is_active=True,
        is_superuser=False,
    )
    return user


@pytest.fixture
def review(user, movie) -> Review:
    review = Review.objects.create(user=user, text="test review", movie=movie)
    return review


@pytest.fixture
def rating(user, movie) -> Raiting:
    rating = Raiting.objects.create(user=user, movie=movie, rating=5)
    return rating
