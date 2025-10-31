"""
Verification and AI models for incident validation
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class AIVerificationResult(models.Model):
    """AI verification results from computer vision models"""
    CLASSIFICATION_TYPES = [
        ('accident', _('Accident')),
        ('hazard', _('Hazard')),
        ('obstruction', _('Obstruction')),
        ('vandalism', _('Vandalism')),
        ('false', _('False Report')),
        ('unknown', _('Unknown')),
    ]
    
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='ai_results')
    
    # Model info
    model_version = models.CharField(_('model version'), max_length=50, default='v1.0')
    model_name = models.CharField(_('model name'), max_length=100, default='YOLOv8')
    
    # Results
    classification_result = models.CharField(_('classification'), max_length=50, choices=CLASSIFICATION_TYPES)
    confidence_score = models.DecimalField(_('confidence score'), max_digits=5, decimal_places=2,
                                          help_text=_('0-100% confidence'))
    
    # Additional metrics
    duplicate_detection_score = models.DecimalField(_('duplicate detection score'), max_digits=5, decimal_places=2,
                                                   null=True, blank=True)
    credibility_score = models.DecimalField(_('credibility score'), max_digits=5, decimal_places=2,
                                           null=True, blank=True)
    
    # Processing metadata
    processing_time = models.DecimalField(_('processing time (seconds)'), max_digits=8, decimal_places=3,
                                         null=True, blank=True)
    model_metadata = JSONField(_('model metadata'), default=dict, blank=True,
                              help_text=_('Additional model-specific metadata'))
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'ai_verification_results'
        verbose_name = _('AI verification result')
        verbose_name_plural = _('AI verification results')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.incident.incident_id} - {self.classification_result} ({self.confidence_score}%)"


class ReviewType(models.TextChoices):
    """Review type enumeration"""
    VERIFICATION = 'verification', _('Verification')
    QA = 'qa', _('Quality Assurance')
    AUDIT = 'audit', _('Audit')


class ReviewStatus(models.TextChoices):
    """Review status enumeration"""
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    FLAGGED = 'flagged', _('Flagged')
    PENDING = 'pending', _('Pending')


class HumanReview(models.Model):
    """Human review of incidents"""
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='human_reviews')
    reviewer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    
    review_type = models.CharField(_('review type'), max_length=20, choices=ReviewType.choices,
                                  default=ReviewType.VERIFICATION)
    review_status = models.CharField(_('review status'), max_length=20, choices=ReviewStatus.choices,
                                     default=ReviewStatus.PENDING)
    
    review_notes = models.TextField(_('review notes'), blank=True)
    review_duration_seconds = models.IntegerField(_('review duration (seconds)'), null=True, blank=True)
    
    reviewed_at = models.DateTimeField(_('reviewed at'), auto_now_add=True)
    
    class Meta:
        db_table = 'human_reviews'
        verbose_name = _('human review')
        verbose_name_plural = _('human reviews')
        ordering = ['-reviewed_at']
    
    def __str__(self):
        return f"{self.incident.incident_id} - {self.reviewer.email} ({self.get_review_status_display()})"
