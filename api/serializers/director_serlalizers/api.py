from rest_framework import serializers

from movies.models import Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("name", "description", "image")
