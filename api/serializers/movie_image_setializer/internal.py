from rest_framework import serializers

from movies.models import Movie_image


class MovieImageInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_image
        fields = ("name", "image")
