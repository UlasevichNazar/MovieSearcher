from rest_framework import serializers

from api.serializers.movies.internal import MovieInternalSerializer
from api.serializers.user_serializer.internal import UserInternalSerializer
from movies.models import Review


class ReviewViewSerializer(serializers.ModelSerializer):
    user = UserInternalSerializer(read_only=True)
    movie = MovieInternalSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "text", "created", "movie")


class CreateReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ("text", "movie", "user")
        read_only_fields = ("user",)


class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("text",)
