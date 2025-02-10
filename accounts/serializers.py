from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')  # Make timestamps read-only

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role', 'phone', 'address', 'date_of_birth')
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be read in responses
            'role': {'required': True}  # Ensure role is required during registration
        }

    def create(self, validated_data):
        """Create a new user and associated UserProfile."""
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()  # Save the user instance
        # Create a UserProfile instance linked to the new user
        UserProfile.objects.create(user=user)
        return user