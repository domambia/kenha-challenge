"""Audit logging models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class AuditLog(models.Model):
    """Audit log entries"""
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(_('action type'), max_length=50)
    entity_type = models.CharField(_('entity type'), max_length=50)
    entity_id = models.CharField(_('entity ID'), max_length=100)
    action_details = JSONField(_('action details'), default=dict)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True, db_index=True)
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']

