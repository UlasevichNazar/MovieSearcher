from rest_framework import serializers

from api.serializers.movies_serializers.internal import MovieInternalSerializer
from api.serializers.user_serializer.internal import UserInternalSerializer
from movies.models import Raiting


class RatingSerializer(serializers.ModelSerializer):
    user = UserInternalSerializer(read_only=True)
    movie = MovieInternalSerializer(read_only=True)

    class Meta:
        model = Raiting
        fields = ("user", "movie", "rating")


class CreateRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Raiting
        fields = ("user", "movie", "rating")
