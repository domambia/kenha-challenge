"""Blockchain integration models"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class BlockchainTransaction(models.Model):
    """Blockchain transaction records"""
    transaction_type = models.CharField(_('transaction type'), max_length=50)
    entity_type = models.CharField(_('entity type'), max_length=50)
    entity_id = models.CharField(_('entity ID'), max_length=100)
    transaction_hash = models.CharField(_('transaction hash'), max_length=66, unique=True)
    block_number = models.BigIntegerField(_('block number'), null=True, blank=True)
    status = models.CharField(_('status'), max_length=20, default='pending')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

