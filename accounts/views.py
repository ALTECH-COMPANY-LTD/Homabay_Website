from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import UserProfile  # Ensure UserProfile is imported
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import jwt  # Import the jwt library
from django.conf import settings  # Import settings to access SECRET_KEY

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profiles."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Override to return the user profile of the authenticated user."""
        return self.get_queryset().get(user=self.request.user)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to add user details to the token response."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user_id'] = user.id  # Ensure user ID is added
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    """View for obtaining JWT tokens with user details."""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """Override to customize the token response."""
        response = super().post(request, *args, **kwargs)

        # Log the token response for debugging
        print("Token Response Data:", response.data)

        # Decode the access token to retrieve user_id
        user_id = self.get_user_id_from_token(response.data['access'])
        print("User ID from Token:", user_id)

        # Retrieve the user based on the user ID
        user = get_object_or_404(User, id=user_id) if user_id else None
        print("User Object:", user)

        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
                'address': user.address,
            }
        else:
            user_data = None

        return Response({
            'refresh': response.data['refresh'],
            'access': response.data['access'],
            'user': user_data,
        })

    def get_user_id_from_token(self, token):
        """Decode the token to get the user_id."""
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token.get('user_id')  # Fetch user_id from decoded token