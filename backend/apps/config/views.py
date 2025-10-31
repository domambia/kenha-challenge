"""
Configuration views
"""
from rest_framework import viewsets, permissions
from .models import SystemConfiguration, IntegrationConfiguration
from .serializers import SystemConfigurationSerializer, IntegrationConfigurationSerializer


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """System configuration management"""
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO: Add admin permission check
    lookup_field = 'key'


class IntegrationConfigurationViewSet(viewsets.ModelViewSet):
    """Integration configuration management"""
    queryset = IntegrationConfiguration.objects.all()
    serializer_class = IntegrationConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO: Add admin permission check
