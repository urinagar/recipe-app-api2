"""
Views for the user API.
"""
from rest_framework import (
    generics,
    permissions,
    authentication,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class UpdateAndRetrieveUserView(generics.RetrieveUpdateAPIView):
    """Update a existing user in the system."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for users."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES