"""Configuration and taxonomy models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class SystemConfiguration(models.Model):
    """System configuration key-value pairs"""
    key = models.CharField(_('key'), max_length=100, unique=True, db_index=True)
    value = models.TextField(_('value'))
    value_type = models.CharField(_('value type'), max_length=20, choices=[
        ('string', _('String')),
        ('integer', _('Integer')),
        ('boolean', _('Boolean')),
        ('json', _('JSON')),
    ], default='string')
    category = models.CharField(_('category'), max_length=50, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_editable = models.BooleanField(_('is editable'), default=True)
    requires_restart = models.BooleanField(_('requires restart'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'system_configurations'
        verbose_name = _('system configuration')
        verbose_name_plural = _('system configurations')
    
    def __str__(self):
        return f"{self.key} = {self.value}"


class IntegrationConfiguration(models.Model):
    """Integration configuration for external systems"""
    INTEGRATION_TYPES = [
        ('rfid', _('RFID')),
        ('cctv', _('CCTV')),
        ('sensor', _('Sensor')),
        ('mapping', _('Mapping')),
        ('sms', _('SMS')),
        ('email', _('Email')),
        ('blockchain', _('Blockchain')),
    ]
    
    integration_type = models.CharField(_('integration type'), max_length=20, choices=INTEGRATION_TYPES)
    name = models.CharField(_('name'), max_length=100)
    configuration = JSONField(_('configuration'), default=dict,
                             help_text=_('API keys, endpoints, credentials (encrypted)'))
    is_active = models.BooleanField(_('is active'), default=True)
    
    last_sync_at = models.DateTimeField(_('last sync at'), null=True, blank=True)
    sync_status = models.CharField(_('sync status'), max_length=20, default='unknown')
    error_message = models.TextField(_('error message'), blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'integration_configurations'
        verbose_name = _('integration configuration')
        verbose_name_plural = _('integration configurations')
    
    def __str__(self):
        return f"{self.get_integration_type_display()} - {self.name}"
