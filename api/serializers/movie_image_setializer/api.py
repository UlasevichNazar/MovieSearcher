from rest_framework import serializers

from movies.models import Movie_image


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_image
        fields = "__all__"
