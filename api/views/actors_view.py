from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsManager
from api.serializers.actors.api import ActorSerializer
from movies.models import Actor


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return Response(
                {"detail": "Query parameters are not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().list(request, *args, **kwargs)


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
