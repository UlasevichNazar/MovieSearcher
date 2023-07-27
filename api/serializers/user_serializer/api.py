from rest_framework import serializers

from user.models import User


class DeleteUserSerializer(serializers.BaseSerializer):
    class Meta:
        model = User
        fields = ("username",)


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "free_mailing_list")
