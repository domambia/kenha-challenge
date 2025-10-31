"""
Verification URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIVerificationResultViewSet, HumanReviewViewSet

app_name = 'verification'

router = DefaultRouter()
router.register(r'ai-results', AIVerificationResultViewSet, basename='ai-result')
router.register(r'reviews', HumanReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
