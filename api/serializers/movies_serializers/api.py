from rest_framework import serializers

from api.serializers.director_serlalizers.internal import DirectorInternalSerializer
from movies.models import Movie


class MovieViewSerializer(serializers.ModelSerializer):
    director = DirectorInternalSerializer(read_only=True)

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
            "publish",
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
