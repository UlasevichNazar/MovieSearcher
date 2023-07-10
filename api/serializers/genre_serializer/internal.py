from rest_framework import serializers

from movies.models import Genre


class GenreInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)
