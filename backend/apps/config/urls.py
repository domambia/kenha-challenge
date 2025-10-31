"""
Configuration URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemConfigurationViewSet, IntegrationConfigurationViewSet

app_name = 'config'

router = DefaultRouter()
router.register(r'system', SystemConfigurationViewSet, basename='system-config')
router.register(r'integrations', IntegrationConfigurationViewSet, basename='integration-config')

urlpatterns = [
    path('', include(router.urls)),
]
