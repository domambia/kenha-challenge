"""
Response coordination models for incident assignment and tracking
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class AssignmentStatus(models.TextChoices):
    """Assignment status enumeration"""
    PENDING = 'pending', _('Pending')
    ACCEPTED = 'accepted', _('Accepted')
    REJECTED = 'rejected', _('Rejected')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')


class IncidentAssignment(models.Model):
    """Incident assignments to responders"""
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_incidents')
    
    assignment_type = models.CharField(_('assignment type'), max_length=20, choices=[
        ('primary', _('Primary')),
        ('backup', _('Backup')),
        ('specialist', _('Specialist')),
    ], default='primary')
    
    status = models.CharField(_('status'), max_length=20, choices=AssignmentStatus.choices, default=AssignmentStatus.PENDING)
    
    # Timestamps
    assigned_at = models.DateTimeField(_('assigned at'), auto_now_add=True)
    accepted_at = models.DateTimeField(_('accepted at'), null=True, blank=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    
    # Routing & ETA
    estimated_arrival_time = models.DateTimeField(_('estimated arrival time'), null=True, blank=True)
    actual_arrival_time = models.DateTimeField(_('actual arrival time'), null=True, blank=True)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        db_table = 'incident_assignments'
        verbose_name = _('incident assignment')
        verbose_name_plural = _('incident assignments')
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.incident.incident_id} -> {self.assigned_to.email} ({self.status})"


class MilestoneType(models.TextChoices):
    """Response milestone types"""
    DISPATCHED = 'dispatched', _('Dispatched')
    EN_ROUTE = 'en_route', _('En Route')
    ON_SCENE = 'on_scene', _('On Scene')
    TRANSPORTING = 'transporting', _('Transporting')
    CLEARED = 'cleared', _('Cleared')


class ResponseMilestone(models.Model):
    """Response milestones tracking"""
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='milestones')
    responder = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='milestones')
    assignment = models.ForeignKey(IncidentAssignment, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='milestones')
    
    milestone_type = models.CharField(_('milestone type'), max_length=20, choices=MilestoneType.choices)
    
    # Location at milestone
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Metadata
    notes = models.TextField(_('notes'), blank=True)
    media_attachments = JSONField(_('media attachments'), default=list, blank=True)
    
    # Blockchain
    milestone_hash = models.CharField(_('milestone hash'), max_length=66, null=True, blank=True)
    blockchain_tx_hash = models.CharField(_('blockchain transaction hash'), max_length=66, null=True, blank=True)
    
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        db_table = 'response_milestones'
        verbose_name = _('response milestone')
        verbose_name_plural = _('response milestones')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.incident.incident_id} - {self.get_milestone_type_display()} @ {self.timestamp}"


class ResponderLocation(models.Model):
    """Real-time responder location tracking"""
    responder = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='locations')
    
    # Location
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    
    # Metadata
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True, db_index=True)
    accuracy = models.DecimalField(_('accuracy (meters)'), max_digits=8, decimal_places=2, null=True, blank=True)
    speed = models.DecimalField(_('speed (km/h)'), max_digits=5, decimal_places=2, null=True, blank=True)
    heading = models.DecimalField(_('heading (degrees)'), max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(_('is active'), default=True)
    device_id = models.CharField(_('device ID'), max_length=100, blank=True)
    
    class Meta:
        db_table = 'responder_locations'
        verbose_name = _('responder location')
        verbose_name_plural = _('responder locations')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['responder', '-timestamp']),
            models.Index(fields=['is_active', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.responder.email} @ ({self.latitude}, {self.longitude}) - {self.timestamp}"


class ResponderChecklist(models.Model):
    """Responder checklists and protocol guidance"""
    incident_type = models.ForeignKey('incidents.IncidentType', on_delete=models.CASCADE, related_name='checklists')
    responder_role = models.CharField(_('responder role'), max_length=30,
                                      help_text=_('Role this checklist applies to'))
    
    checklist_items = JSONField(_('checklist items'), default=list,
                               help_text=_('List of checklist items with order, description, required'))
    is_required = models.BooleanField(_('is required'), default=True)
    order = models.IntegerField(_('order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'responder_checklists'
        verbose_name = _('responder checklist')
        verbose_name_plural = _('responder checklists')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.incident_type.name} - {self.responder_role} Checklist"
