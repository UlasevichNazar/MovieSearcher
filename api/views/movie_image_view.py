from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsManager
from api.serializers.movie_image.api import MovieImageSerializer
from movies.models import Movie_image


class MovieImageListView(generics.ListAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return Response(
                {"detail": "Query parameters are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)


class MovieImageCreateView(generics.CreateAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (IsAdminUser, IsManager)


class MovieImageUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie_image.objects.all()
    serializer_class = MovieImageSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
