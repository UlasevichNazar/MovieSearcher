from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.rating_serializers.api import CreateRatingSerializer
from api.serializers.rating_serializers.api import UpdateRatingSerializer
from movies.models import Raiting


@extend_schema_view(
    change_rating=extend_schema(summary="Change rating of film", tags=["Rating"])
)
class RatingView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Raiting.objects.all()

    serializer_action_classes = {
        "create": CreateRatingSerializer,
        "change_rating": UpdateRatingSerializer,
    }

    def get_serializer_context(self):
        return {
            "request": self.request,
        }

    def get_serializer_class(self):
        """Return the serializer class based on the request method"""
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

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

    @action(methods=["patch"], detail=False, url_path="change_rating")
    def change_rating(self, request):
        user = request.user
        movie = request.data.get("movie")
        rating_value = request.data.get("rating")  # noqa: F841

        try:
            rating = Raiting.objects.get(user=user, movie=movie)
            serializer = self.get_serializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                rating = serializer.change_rating(rating, serializer.validated_data)
                return Response({"message": "Rating updated successfully"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                rating = serializer.save()
                return Response(
                    {"message": "Rating created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
