"""
Views for the recipes APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD operations on recipe."""
    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()

    def get_querset(self):
        '''Retrieve recipes for authenticated user.'''
        return self.queryset.filter(user=self.user).order_by('-id')