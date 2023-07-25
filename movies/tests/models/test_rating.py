import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from movies.models import Raiting


@pytest.mark.django_db
class TestRating:
    def test_create_rating_valid_values(self, rating, user, movie):
        assert rating.user == user
        assert rating.movie == movie
        assert rating.rating == 5

    def test_update_rating_valid_value(self, rating):
        rating.rating = 10
        rating.save()
        assert rating.rating == 10

    def test_retrieve_rating(self, rating):
        retrieved_rating = Raiting.objects.get(id=rating.id)
        assert retrieved_rating == rating

    def test_create_rating_invalid_user(self, movie):
        with pytest.raises(IntegrityError):
            rating = Raiting.objects.create(movie=movie, rating=4)
            rating.save()

    def test_create_rating_invalid_movie(self, user):
        with pytest.raises(IntegrityError):
            rating = Raiting.objects.create(user=user, rating=4)
            rating.save()

    def test_create_rating_invalid_rating(self, user, movie):
        with pytest.raises(ValidationError):
            rating = Raiting.objects.create(user=user, movie=movie, rating=11)
            rating.save()

    def test_update_rating_with_invalid_value(self, rating):
        rating.save()
        with pytest.raises(ValidationError):
            rating.rating = -1
            rating.save()

    def test_create_rating_existing_user_and_movie(self, user, movie, rating):
        rating.save()
        with pytest.raises(IntegrityError):
            another_one_rating_by_user = Raiting.objects.create(
                user=user, movie=movie, rating=6
            )
            another_one_rating_by_user.save()
