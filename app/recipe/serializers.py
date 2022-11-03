from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe object."""

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'price',
            'time_minutes',
            'link',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """create and return a recipe."""
        return Recipe.objects.create(**validated_data)