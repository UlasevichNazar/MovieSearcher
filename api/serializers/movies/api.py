from rest_framework import serializers

from api.serializers.actors.internal import ActorInternalSerializer
from api.serializers.category.internal import CategoryInternalSerializer
from api.serializers.director.internal import DirectorInternalSerializer
from api.serializers.genre.internal import GenreInternalSerializer
from api.serializers.movie_image.internal import MovieImageInternalSerializer
from api.serializers.rating.api import RatingSerializer
from api.serializers.rewiew.api import ReviewViewSerializer
from movies.models import Movie


class MovieViewSerializer(serializers.ModelSerializer):
    category = CategoryInternalSerializer(read_only=True)
    poster = serializers.ImageField(
        max_length=None, allow_empty_file=False, use_url=False
    )

    class Meta:
        model = Movie
        fields = (
            "title",
            "poster",
            "category",
            "publish",
        )


class AdminMovieViewSerializer(serializers.ModelSerializer):
    category = CategoryInternalSerializer(read_only=True)
    poster = serializers.ImageField(
        max_length=None, allow_empty_file=False, use_url=False
    )

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "poster",
            "category",
            "publish",
        )


class MovieRetrieveSerializer(serializers.ModelSerializer):
    category = CategoryInternalSerializer(read_only=True)
    genre = GenreInternalSerializer(read_only=True, many=True)
    director = DirectorInternalSerializer(read_only=True)
    actors = ActorInternalSerializer(read_only=True, many=True)
    reviews = ReviewViewSerializer(many=True, read_only=True)
    movie_of_rating = RatingSerializer(many=True, read_only=True)
    movie_images = MovieImageInternalSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            "title",
            "description",
            "poster",
            "category",
            "genre",
            "director",
            "actors",
            "country",
            "year",
            "budget",
            "fees_in_the_world",
            "reviews",
            "movie_of_rating",
            "movie_images",
        )


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "title",
            "description",
            "poster",
            "category",
            "genre",
            "director",
            "actors",
            "country",
            "year",
            "budget",
            "fees_in_the_world",
            "slug",
            "status",
        )


class BeatMoviesSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ("title", "average_rating")
