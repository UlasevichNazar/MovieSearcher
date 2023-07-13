from rest_framework import serializers

from api.serializers.user_serializer.internal import UserForProfileInternalSerializer
from userprofile.models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserForProfileInternalSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("user", "bio", "profile_pic")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserForProfileInternalSerializer()

    class Meta:
        model = Profile
        fields = ("user", "bio", "profile_pic")
