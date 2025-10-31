from django.contrib import admin
from .models import SystemConfiguration, IntegrationConfiguration


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_type', 'category', 'is_editable', 'updated_at']
    list_filter = ['category', 'value_type', 'is_editable']
    search_fields = ['key', 'description']


@admin.register(IntegrationConfiguration)
class IntegrationConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'integration_type', 'is_active', 'sync_status', 'last_sync_at']
    list_filter = ['integration_type', 'is_active', 'sync_status']

