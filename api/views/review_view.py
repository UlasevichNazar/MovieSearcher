from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsManager
from api.permissions import IsOwnerUser
from api.serializers.rewiew.api import CreateReviewSerializer
from api.serializers.rewiew.api import ReviewViewSerializer
from api.serializers.rewiew.api import UpdateReviewSerializer
from movies.models import Review


@extend_schema_view(list=extend_schema(summary="All Reviews", tags=["Review"]))
class ReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewViewSerializer
    permission_classes = (AllowAny,)


@extend_schema_view(create=extend_schema(summary="Create Reviews", tags=["Review"]))
class CreateReviewView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = (IsAuthenticated,)


@extend_schema_view(update=extend_schema(summary="Update Reviews", tags=["Review"]))
class UpdateReviewView(generics.UpdateAPIView):
    serializer_class = UpdateReviewSerializer
    permission_classes = (IsOwnerUser,)
    lookup_field = "pk"

    def get_object(self):
        queryset = Review.objects.filter(user=self.request.user)
        pk = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, **{self.lookup_field: pk})
        return obj


@extend_schema_view(destroy=extend_schema(summary="Destroy Review", tags=["Review"]))
class DestroyReviewView(generics.DestroyAPIView):
    serializer_class = ReviewViewSerializer
    permission_classes = (IsOwnerUser, IsAdminUser, IsManager)
    lookup_field = "pk"

    def get_object(self):
        queryset = Review.objects.filter(user=self.request.user)
        pk = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, **{self.lookup_field: pk})
        return obj
