from django.shortcuts import get_object_or_404
from rest_framework import generics

from api.permissions import IsOwnerUser
from api.serializers.user_profile.api import UserProfileSerializer
from api.serializers.user_profile.api import UserProfileUpdateSerializer
from userprofile.models import Profile


class UserProfileView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerUser,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsOwnerUser,)
    lookup_field = "pk"

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset, **{self.lookup_field: pk})
        return obj
