from rest_framework import serializers

from movies.models import Director


class DirectorInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("name",)
