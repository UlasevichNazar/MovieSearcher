from django.db.models import Avg
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsManager
from api.serializers.movies.api import AdminMovieViewSerializer
from api.serializers.movies.api import BeatMoviesSerializer
from api.serializers.movies.api import MovieCreateUpdateSerializer
from api.serializers.movies.api import MovieRetrieveSerializer
from api.serializers.movies.api import MovieViewSerializer
from api.service import MovieFilter
from movies.models import Movie


@extend_schema_view(
    list=extend_schema(summary="All movies", tags=["Movie"]),
)
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.filter(status=Movie.Status.PUBLISHED)
    serializer_class = MovieViewSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return AdminMovieViewSerializer
        return MovieViewSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return Response(
                {"detail": "Query parameters are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(summary="Create movie", tags=["Movie"]),
)
class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = (IsAdminUser, IsManager)


@extend_schema_view(
    retrieve=extend_schema(summary="Get movie", tags=["Movie"]),
)
class MovieRetrieveView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MovieRetrieveSerializer
    lookup_field = "slug"

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, **{self.lookup_field: slug})
        return obj


@extend_schema_view(
    update=extend_schema(summary="Update movie", tags=["Movie"]),
    partial_update=extend_schema(summary="Partial update of movie", tags=["Movie"]),
    destroy=extend_schema(summary="Destroy movie", tags=["Movie"]),
)
class MovieUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    permission_classes = (IsAdminUser, IsManager)
    serializer_class = MovieCreateUpdateSerializer

    lookup_field = "slug"

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, **{self.lookup_field: slug})
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BestMoviesView(generics.ListAPIView):
    queryset = (
        Movie.objects.filter(status=Movie.Status.PUBLISHED)
        .exclude(
            Q(movie_of_rating__isnull=True) | Q(movie_of_rating__rating__isnull=True)
        )
        .annotate(average_rating=Avg("movie_of_rating__rating"))
        .order_by("-average_rating")
    )
    serializer_class = BeatMoviesSerializer
