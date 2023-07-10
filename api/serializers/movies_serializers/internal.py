from rest_framework import serializers

from movies.models import Movie


class MovieInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title",)
