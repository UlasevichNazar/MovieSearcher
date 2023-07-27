from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.genre.api import GenreSerializer
from movies.models import Genre


class CreateGenreView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser, IsManager)


class UpdateDeleteGenre(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
