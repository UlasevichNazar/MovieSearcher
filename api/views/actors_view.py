from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.actors_serializer.api import ActorSerializer
from movies.models import Actor


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (AllowAny,)


class ActorRetrieveView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"


class ActorCreateView(generics.CreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminUser, IsManager)


class ActorUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
