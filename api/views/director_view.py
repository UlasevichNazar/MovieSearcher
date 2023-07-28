from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsManager
from api.serializers.director.api import DirectorSerializer
from movies.models import Director


class DirectorListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return Response(
                {"detail": "Query parameters are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)


class DirectorRetrieveView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"


class DirectorCreateView(generics.CreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (IsAdminUser, IsManager)


class DirectorUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
