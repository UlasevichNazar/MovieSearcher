from rest_framework import serializers

from user.admin import User


class UserInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
