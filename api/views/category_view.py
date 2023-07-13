from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.category.api import CategorySerializer
from movies.models import Category


class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser, IsManager)


class UpdateDeleteCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
