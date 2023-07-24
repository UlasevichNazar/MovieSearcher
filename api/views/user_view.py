from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.permissions import IsManager
from api.serializers.user_serializer.api import AllUsersSerializer
from api.serializers.user_serializer.api import DeleteUserSerializer


class GetUserView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = AllUsersSerializer
    permission_classes = (IsAdminUser, IsManager)


class DeleteUserView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = DeleteUserSerializer
    permission_classes = (IsAdminUser, IsManager)
    lookup_field = "pk"
