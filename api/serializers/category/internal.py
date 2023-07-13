from rest_framework import serializers

from movies.models import Category


class CategoryInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)
