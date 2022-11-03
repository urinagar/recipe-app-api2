"""
Tests for recipe API's.
"""
from django.test import TestCase
from decimal import Decimal
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from recipe.serializers import RecipeSerializer

from core import models

RECIPES_URL = reverse('recipe:recipe-list')

def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)

def create_recipe(user, **params):
    """Creating recipes for tests"""
    defaults = {
        'title': 'title1',
        'description': 'desc 1',
        'time_minutes': 5,
        'price': Decimal('2.5'),
        'link': 'example2.com'
    }
    defaults.update(params)
    return models.Recipe.objects.create(user=user, **defaults)

class PublicRecipeTests(TestCase):
    """Tests for unautherized users."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test Creating a recipe for the unauthenticated user."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeTests(TestCase):
    """Tests for authenticated users."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes_list(self):
        """Test get all method for authenticated users."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = models.Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)
        print(serializer.data)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test recipes recived only for the authenticated user."""
        other_user = create_user(email='test2@example.com')
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPES_URL)

        recipes = models.Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
