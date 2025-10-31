"""Work order and maintenance models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class WorkOrder(models.Model):
    """Work orders for infrastructure maintenance"""
    WORK_TYPES = [
        ('inspection', _('Inspection')),
        ('repair', _('Repair')),
        ('maintenance', _('Maintenance')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('assigned', _('Assigned')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    incident = models.ForeignKey('incidents.Incident', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='work_orders')
    work_type = models.CharField(_('work type'), max_length=20, choices=WORK_TYPES)
    
    assigned_to = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='work_orders')
    assigned_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_work_orders')
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(_('priority'), max_length=20, default='medium')
    
    description = models.TextField(_('description'))
    
    # Location
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    
    # Duration
    estimated_duration = models.IntegerField(_('estimated duration (minutes)'), null=True, blank=True)
    actual_duration = models.IntegerField(_('actual duration (minutes)'), null=True, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(_('started at'), null=True, blank=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    
    # Completion
    completion_notes = models.TextField(_('completion notes'), blank=True)
    media_attachments = JSONField(_('media attachments'), default=list, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'work_orders'
        verbose_name = _('work order')
        verbose_name_plural = _('work orders')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Work Order #{self.id} - {self.get_work_type_display()}"


class InfrastructureInspection(models.Model):
    """Infrastructure inspection records"""
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='inspections')
    inspector = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    inspection_date = models.DateTimeField(_('inspection date'))
    inspection_type = models.CharField(_('inspection type'), max_length=50)
    
    damage_assessment = JSONField(_('damage assessment'), default=dict, blank=True)
    repair_needed = models.BooleanField(_('repair needed'), default=False)
    priority = models.CharField(_('priority'), max_length=20, default='medium')
    
    photos = JSONField(_('photos'), default=list, blank=True)
    inspection_report = models.TextField(_('inspection report'), blank=True)
    
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'infrastructure_inspections'
        verbose_name = _('infrastructure inspection')
        verbose_name_plural = _('infrastructure inspections')
    
    def __str__(self):
        return f"Inspection {self.id} - {self.work_order}"
