"""Notification models"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """User notifications"""
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(_('type'), max_length=50)
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))
    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

