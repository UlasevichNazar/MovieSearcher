import pytest
from django.db.utils import IntegrityError

from movies.models import Review


@pytest.mark.django_db
class TestReview:
    def test_create_review_valid_data(self, review, movie):
        assert movie.reviews.get(text="test review") == review

    def test_delete_review(self, review):
        review.delete()
        assert review not in Review.objects.all()

    def test_create_review_invalid_user(self, movie):
        with pytest.raises(IntegrityError):
            review = Review.objects.create(text="test review", movie=movie)
            review.save()

    def test_create_review_invalid_movie(self, user):
        with pytest.raises(IntegrityError):
            review = Review.objects.create(
                user=user,
                text="test review",
            )
            review.save()

    def test_create_review_empty_text(self, user, movie):
        with pytest.raises(ValueError):
            review = Review.objects.create(
                user=user,
                text="",
                movie=movie,
            )
            review.save()

    def test_retrieve_review_invalid_id(self):
        with pytest.raises(Review.DoesNotExist):
            Review.objects.get(id=0)
