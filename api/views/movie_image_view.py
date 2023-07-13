from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.movie_image_setializer.api import MovieImageSerializer
from movies.models import Movie_image


class MovieImageListView(generics.ListAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (AllowAny,)


class MovieImageCreateView(generics.CreateAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (IsAdminUser, IsManager)


class MovieImageUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
