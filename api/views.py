from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from api.serializers.movies_serializers.api import MovieCreateUpdateSerializer
from api.serializers.movies_serializers.api import MovieViewSerializer
from movies.models import Movie


@extend_schema_view(
    list=extend_schema(summary="All movies", tags=["Movie"]),
    create=extend_schema(summary="Create movie", tags=["Movie"]),
    update=extend_schema(summary="Update movie", tags=["Movie"]),
    partial_update=extend_schema(summary="Partial update of movie", tags=["Movie"]),
    retrieve=extend_schema(summary="Get movie", tags=["Movie"]),
    desctroy=extend_schema(summary="Destroy movie", tags=["Movie"]),
)
class MovieView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_action_classes = {
        "create": (IsAdminUser,),
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
    }

    queryset = Movie.objects.all()
    serializer_action_classes = {
        "create": MovieCreateUpdateSerializer,
        "list": MovieViewSerializer,
        "retrieve": MovieViewSerializer,
        "update": MovieCreateUpdateSerializer,
        "destroy": MovieViewSerializer,
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (AllowAny,)
            )
        ]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
