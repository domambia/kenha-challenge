"""
Authentication and user management URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    OTPVerificationView,
    ResendOTPView,
    UserProfileView,
    UserListView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView, name='register'),
    path('login/', UserLoginView, name='login'),
    path('logout/', UserLogoutView, name='logout'),
    path('verify-otp/', OTPVerificationView, name='verify-otp'),
    path('resend-otp/', ResendOTPView, name='resend-otp'),
    path('me/', UserProfileView.as_view(), name='me'),  # Class-based view
    path('users/', UserListView.as_view(), name='user-list'),  # Class-based view
]

