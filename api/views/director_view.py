from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.director.api import DirectorSerializer
from movies.models import Director


class DirectorListView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (AllowAny,)


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
