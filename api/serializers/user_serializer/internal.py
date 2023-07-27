from rest_framework import serializers

from user.admin import User


class UserInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserForProfileInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "free_mailing_list", "last_login")
