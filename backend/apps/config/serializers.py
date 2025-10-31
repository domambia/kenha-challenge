"""
Configuration serializers
"""
from rest_framework import serializers
from .models import SystemConfiguration, IntegrationConfiguration


class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = ['id', 'key', 'value', 'value_type', 'category', 'description',
                 'is_editable', 'requires_restart']
        read_only_fields = ['id']


class IntegrationConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationConfiguration
        fields = ['id', 'integration_type', 'name', 'is_active', 'sync_status',
                 'last_sync_at', 'error_message']
        read_only_fields = ['id', 'last_sync_at', 'error_message']
