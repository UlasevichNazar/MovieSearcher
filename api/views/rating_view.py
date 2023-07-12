from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.rating_serializers.api import CreateRatingSerializer
from movies.models import Raiting


class CreateRatingView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateRatingSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        movie = request.data.get("movie")
        if Raiting.objects.filter(user=request.user, movie=movie).exists():
            return Response(
                {"detail": "Rating already exists for this movie."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CreateRatingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Rating saved successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Invalid rating data."},
                status=status.HTTP_400_BAD_REQUEST,
            )
