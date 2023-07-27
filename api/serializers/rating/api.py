from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from rest_framework import serializers

from api.serializers.movies.internal import MovieInternalSerializer
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


class UpdateRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        model = Raiting
        fields = ("user", "movie", "rating")

    def change_rating(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.save()
        return instance
