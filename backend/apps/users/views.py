"""
User authentication and management views
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserProfile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def UserRegistrationView(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generate OTP and send (implementation needed)
        # For now, return success
        return Response({
            'message': 'Registration successful. Please verify OTP.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def UserLoginView(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def UserLogoutView(request):
    """User logout endpoint"""
    # TODO: Implement token blacklisting
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def OTPVerificationView(request):
    """OTP verification endpoint"""
    # TODO: Implement OTP verification logic
    return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def ResendOTPView(request):
    """Resend OTP endpoint"""
    # TODO: Implement OTP resend logic
    return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user profile"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """List users (admin only)"""
    permission_classes = [permissions.IsAuthenticated]  # TODO: Add admin permission check
    queryset = User.objects.all()
    serializer_class = UserSerializer

