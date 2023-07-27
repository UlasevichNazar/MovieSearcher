from rest_framework import serializers

from movies.models import Actor


class ActorInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("name",)
