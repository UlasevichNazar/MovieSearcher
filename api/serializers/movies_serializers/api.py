from rest_framework import serializers

from api.serializers.actors_serializer.internal import ActorInternalSerializer
from api.serializers.category_serializer.api import CategorySerializer
from api.serializers.category_serializer.internal import CategoryInternalSerializer
from api.serializers.director_serlalizers.api import DirectorSerializer
from api.serializers.director_serlalizers.internal import DirectorInternalSerializer
from api.serializers.genre_serializer.api import GenreSerializer
from api.serializers.genre_serializer.internal import GenreInternalSerializer
from api.serializers.movie_image_setializer.internal import MovieImageInternalSerializer
from api.serializers.rating_serializers.api import RatingSerializer
from api.serializers.rewiew_serializer.api import ReviewViewSerializer
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
    actors = ActorInternalSerializer(many=True)
    director = DirectorSerializer()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

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
