"""
User serializers
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, UserReputation


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'password_confirm', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'role', 
                  'is_verified', 'reputation_score', 'profile', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined', 'reputation_score']
    
    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'department': obj.profile.department,
                'organization': obj.profile.organization,
                'language': obj.profile.language,
            }
        return None


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer"""
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'role', 
                  'is_verified', 'reputation_score', 'date_joined']
        read_only_fields = ['id', 'date_joined']

