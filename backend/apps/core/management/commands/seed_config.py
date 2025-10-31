"""
Management command to seed system and integration configurations
"""
from django.core.management.base import BaseCommand
from apps.config.models import SystemConfiguration, IntegrationConfiguration
import json


class Command(BaseCommand):
    help = 'Seed system and integration configurations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting configuration seeding...'))
        
        # System Configurations
        system_configs = [
            {
                'key': 'system.name',
                'value': 'KeNHA eSafety Platform',
                'value_type': 'string',
                'category': 'General',
                'description': 'System name',
                'is_editable': False,
            },
            {
                'key': 'system.version',
                'value': '1.0.0',
                'value_type': 'string',
                'category': 'General',
                'description': 'System version',
                'is_editable': False,
            },
            {
                'key': 'incidents.default_severity',
                'value': 'P3',
                'value_type': 'string',
                'category': 'Incidents',
                'description': 'Default severity for new incidents',
                'is_editable': True,
            },
            {
                'key': 'incidents.auto_verify_threshold',
                'value': '85',
                'value_type': 'integer',
                'category': 'Incidents',
                'description': 'AI confidence score threshold for auto-verification',
                'is_editable': True,
            },
            {
                'key': 'notifications.enable_sms',
                'value': 'true',
                'value_type': 'boolean',
                'category': 'Notifications',
                'description': 'Enable SMS notifications',
                'is_editable': True,
            },
            {
                'key': 'notifications.enable_email',
                'value': 'true',
                'value_type': 'boolean',
                'category': 'Notifications',
                'description': 'Enable email notifications',
                'is_editable': True,
            },
            {
                'key': 'blockchain.enabled',
                'value': 'true',
                'value_type': 'boolean',
                'category': 'Blockchain',
                'description': 'Enable blockchain integration',
                'is_editable': True,
            },
            {
                'key': 'reputation.minimum_score',
                'value': '30.0',
                'value_type': 'string',
                'category': 'Reputation',
                'description': 'Minimum reputation score for user reports',
                'is_editable': True,
            },
            {
                'key': 'response.max_responders_per_incident',
                'value': '5',
                'value_type': 'integer',
                'category': 'Response',
                'description': 'Maximum number of responders per incident',
                'is_editable': True,
            },
            {
                'key': 'iot.data_retention_days',
                'value': '90',
                'value_type': 'integer',
                'category': 'IoT',
                'description': 'Number of days to retain IoT data',
                'is_editable': True,
            },
            {
                'key': 'analytics.report_generation_interval',
                'value': 'daily',
                'value_type': 'string',
                'category': 'Analytics',
                'description': 'Interval for generating analytics reports',
                'is_editable': True,
            },
            {
                'key': 'security.mfa_required_roles',
                'value': json.dumps(['super_admin', 'system_admin', 'tmc_operator', 'dispatcher']),
                'value_type': 'json',
                'category': 'Security',
                'description': 'Roles that require MFA',
                'is_editable': True,
            },
        ]
        
        created_configs = 0
        for config_data in system_configs:
            config, created = SystemConfiguration.objects.get_or_create(
                key=config_data['key'],
                defaults=config_data
            )
            if created:
                created_configs += 1
                self.stdout.write(f'Created system configuration: {config.key}')
        
        # Integration Configurations
        integration_configs = [
            {
                'integration_type': 'rfid',
                'name': 'RFID System Main',
                'configuration': {
                    'api_endpoint': 'https://api.kenha.ke/rfid',
                    'api_key': 'encrypted_key_placeholder',
                    'mqtt_broker': 'mqtt.kenha.ke',
                    'mqtt_port': 1883,
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'cctv',
                'name': 'CCTV Network Primary',
                'configuration': {
                    'api_endpoint': 'https://api.kenha.ke/cctv',
                    'api_key': 'encrypted_key_placeholder',
                    'storage_bucket': 'kenha-cctv-recordings',
                    'retention_days': 30,
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'sensor',
                'name': 'Sensor Network Main',
                'configuration': {
                    'api_endpoint': 'https://api.kenha.ke/sensors',
                    'api_key': 'encrypted_key_placeholder',
                    'mqtt_broker': 'mqtt.kenha.ke',
                    'mqtt_port': 1883,
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'sms',
                'name': 'SMS Provider - Twilio',
                'configuration': {
                    'provider': 'twilio',
                    'account_sid': 'encrypted_sid_placeholder',
                    'auth_token': 'encrypted_token_placeholder',
                    'from_number': '+254XXXXXXXXX',
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'email',
                'name': 'Email Service - SMTP',
                'configuration': {
                    'smtp_host': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'smtp_username': 'encrypted_username_placeholder',
                    'smtp_password': 'encrypted_password_placeholder',
                    'from_email': 'noreply@kenha.ke',
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'blockchain',
                'name': 'Blockchain Network - Base Sepolia',
                'configuration': {
                    'network': 'base-sepolia',
                    'rpc_url': 'https://sepolia.base.org',
                    'relayer_address': 'encrypted_address_placeholder',
                    'relayer_private_key': 'encrypted_key_placeholder',
                    'enabled': True,
                },
                'is_active': True,
            },
            {
                'integration_type': 'mapping',
                'name': 'Mapping Service - Google Maps',
                'configuration': {
                    'provider': 'google',
                    'api_key': 'encrypted_key_placeholder',
                    'geocoding_enabled': True,
                    'routing_enabled': True,
                    'enabled': True,
                },
                'is_active': True,
            },
        ]
        
        created_integrations = 0
        for int_config_data in integration_configs:
            integration, created = IntegrationConfiguration.objects.get_or_create(
                integration_type=int_config_data['integration_type'],
                name=int_config_data['name'],
                defaults=int_config_data
            )
            if created:
                created_integrations += 1
                self.stdout.write(f'Created integration configuration: {integration.name}')
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_configs} system configurations '
            f'and {created_integrations} integration configurations'
        ))

