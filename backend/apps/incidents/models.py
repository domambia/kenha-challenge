"""
Incident models for eSafety platform
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.core.validators import MinLengthValidator


class IncidentType(models.Model):
    """Incident type taxonomy"""
    name = models.CharField(_('name'), max_length=100, unique=True)
    category = models.CharField(_('category'), max_length=50, choices=[
        ('accident', _('Accident')),
        ('hazard', _('Hazard')),
        ('infrastructure', _('Infrastructure')),
        ('other', _('Other')),
    ])
    severity_template = models.CharField(_('default severity'), max_length=10, default='P3')
    default_sla_minutes = models.IntegerField(_('default SLA minutes'), default=60)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'incident_types'
        verbose_name = _('incident type')
        verbose_name_plural = _('incident types')
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.category} - {self.name}"


class IncidentSeverity(models.Model):
    """Incident severity levels"""
    level = models.CharField(_('severity level'), max_length=10, unique=True)  # P1, P2, P3, P4
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'))
    response_time_target_minutes = models.IntegerField(_('response time target (minutes)'))
    escalation_time_minutes = models.IntegerField(_('escalation time (minutes)'))
    color_code = models.CharField(_('color code'), max_length=7, default='#FF0000')
    priority_score = models.IntegerField(_('priority score'), help_text=_('Higher = more priority'))
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        db_table = 'incident_severities'
        verbose_name = _('incident severity')
        verbose_name_plural = _('incident severities')
        ordering = ['priority_score']
    
    def __str__(self):
        return f"{self.level} - {self.name}"


class IncidentStatus(models.TextChoices):
    """Incident status enumeration"""
    PENDING = 'pending', _('Pending')
    VERIFIED = 'verified', _('Verified')
    ASSIGNED = 'assigned', _('Assigned')
    IN_PROGRESS = 'in_progress', _('In Progress')
    RESOLVED = 'resolved', _('Resolved')
    CLOSED = 'closed', _('Closed')
    FALSE = 'false', _('False Report')


class VerificationStatus(models.TextChoices):
    """Verification status enumeration"""
    PENDING = 'pending', _('Pending')
    VERIFIED = 'verified', _('Verified')
    FALSE = 'false', _('False')


class Incident(models.Model):
    """
    Core incident model representing road incidents reported by citizens or detected by systems
    """
    # Identification
    incident_id = models.CharField(_('incident ID'), max_length=50, unique=True, db_index=True)
    
    # Classification
    incident_type = models.ForeignKey(IncidentType, on_delete=models.PROTECT, related_name='incidents')
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.PROTECT, related_name='incidents')
    status = models.CharField(_('status'), max_length=20, choices=IncidentStatus.choices, default=IncidentStatus.PENDING)
    
    # Reporting
    reporter = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_incidents')
    is_anonymous = models.BooleanField(_('anonymous report'), default=False)
    description = models.TextField(_('description'), validators=[MinLengthValidator(20)])
    
    # Location (PostGIS PointField - will be activated when PostGIS is installed)
    # For now, using DecimalField for lat/lng
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    road_classification = models.CharField(_('road classification'), max_length=50, blank=True)
    road_name = models.CharField(_('road name'), max_length=200, blank=True)
    nearest_milestone = models.CharField(_('nearest milestone'), max_length=100, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(_('incident timestamp'))
    weather = models.CharField(_('weather'), max_length=50, blank=True)
    lane_count = models.IntegerField(_('lane count'), null=True, blank=True)
    vehicles_involved_count = models.IntegerField(_('vehicles involved'), default=0)
    has_injuries = models.BooleanField(_('has injuries'), default=False)
    infrastructure_damage_tags = JSONField(_('infrastructure damage tags'), default=list, blank=True)
    
    # Verification
    verification_status = models.CharField(_('verification status'), max_length=20, 
                                         choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    ai_confidence_score = models.DecimalField(_('AI confidence score'), max_digits=5, decimal_places=2, 
                                             null=True, blank=True, help_text=_('0-100'))
    verified_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='verified_incidents')
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    
    # Duplicate Detection
    parent_incident = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='duplicate_incidents')
    is_duplicate = models.BooleanField(_('is duplicate'), default=False)
    
    # SLA Management
    sla_start_time = models.DateTimeField(_('SLA start time'), null=True, blank=True)
    sla_target_time = models.DateTimeField(_('SLA target time'), null=True, blank=True)
    sla_breach_time = models.DateTimeField(_('SLA breach time'), null=True, blank=True)
    escalation_level = models.IntegerField(_('escalation level'), default=0)
    
    # Blockchain
    incident_hash = models.CharField(_('incident hash'), max_length=66, null=True, blank=True)
    blockchain_tx_hash = models.CharField(_('blockchain transaction hash'), max_length=66, null=True, blank=True)
    blockchain_timestamp = models.DateTimeField(_('blockchain timestamp'), null=True, blank=True)
    blockchain_block_number = models.BigIntegerField(_('blockchain block number'), null=True, blank=True)
    
    # Resolution
    resolution_notes = models.TextField(_('resolution notes'), blank=True)
    resolved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='resolved_incidents')
    resolved_at = models.DateTimeField(_('resolved at'), null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'incidents'
        verbose_name = _('incident')
        verbose_name_plural = _('incidents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'severity']),
            models.Index(fields=['verification_status', 'ai_confidence_score']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.incident_id} - {self.incident_type.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            # Generate unique incident ID
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.incident_id = f"INC-{timestamp}-{self.pk or 'TEMP'}"
        super().save(*args, **kwargs)


class IncidentComment(models.Model):
    """Comments on incidents"""
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='incident_comments')
    comment_text = models.TextField(_('comment'))
    comment_type = models.CharField(_('comment type'), max_length=20, choices=[
        ('internal', _('Internal')),
        ('public', _('Public')),
    ], default='internal')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='replies')
    is_edited = models.BooleanField(_('is edited'), default=False)
    edited_at = models.DateTimeField(_('edited at'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'incident_comments'
        verbose_name = _('incident comment')
        verbose_name_plural = _('incident comments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.email} on {self.incident.incident_id}"


class IncidentMessage(models.Model):
    """Messages between users regarding incidents"""
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='received_messages')
    message_text = models.TextField(_('message'))
    message_type = models.CharField(_('message type'), max_length=20, choices=[
        ('chat', _('Chat')),
        ('follow_up', _('Follow-up')),
        ('request', _('Request')),
    ], default='chat')
    is_read = models.BooleanField(_('is read'), default=False)
    read_at = models.DateTimeField(_('read at'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'incident_messages'
        verbose_name = _('incident message')
        verbose_name_plural = _('incident messages')
        ordering = ['-created_at']

