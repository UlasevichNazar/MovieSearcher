from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.movies_serializers.api import AdminMovieViewSerializer
from api.serializers.movies_serializers.api import MovieCreateUpdateSerializer
from api.serializers.movies_serializers.api import MovieRetrieveSerializer
from api.serializers.movies_serializers.api import MovieViewSerializer
from movies.models import Actor
from movies.models import Category
from movies.models import Director
from movies.models import Genre
from movies.models import Movie


@extend_schema_view(
    list=extend_schema(summary="All movies", tags=["Movie"]),
)
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieViewSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return AdminMovieViewSerializer
        return MovieViewSerializer


@extend_schema_view(
    create=extend_schema(summary="Create movie", tags=["Movie"]),
)
class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        # Сохранение связей (актер, режиссер, жанры, категории)
        actor_data = serializer.validated_data.pop("actors", None)
        director_data = serializer.validated_data.pop("director", None)
        genre_data = serializer.validated_data.pop("genre", None)
        category_data = serializer.validated_data.pop("category", None)

        # Сохранение фильма
        movie = serializer.save()

        # Сохранение актера
        if actor_data:
            if isinstance(actor_data, str):
                actor, _ = Actor.objects.get_or_create(name=actor_data)
            else:
                actor, _ = Actor.objects.get_or_create(
                    name=actor_data["name"], defaults=actor_data
                )
            movie.actors.add(actor)

        # Сохранение режиссера
        if director_data:
            if isinstance(director_data, str):
                director, _ = Director.objects.get_or_create(name=director_data)
            else:
                director, _ = Director.objects.get_or_create(
                    name=director_data["name"], defaults=director_data
                )
            movie.director = director

        # Сохранение жанра
        if genre_data:
            if isinstance(genre_data, str):
                genre, _ = Genre.objects.get_or_create(name=genre_data)
            else:
                genre, _ = Genre.objects.get_or_create(
                    name=genre_data["name"], defaults=genre_data
                )
            movie.genre.add(genre)

        # Сохранение категории
        if category_data:
            if isinstance(category_data, str):
                category, _ = Category.objects.get_or_create(name=category_data)
            else:
                category, _ = Category.objects.get_or_create(name=category_data["name"])
            movie.category.set([category])


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
