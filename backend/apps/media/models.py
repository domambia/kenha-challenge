"""
Media and evidence models
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class MediaAsset(models.Model):
    """Media assets (photos, videos, audio) attached to incidents"""
    ASSET_TYPES = [
        ('photo', _('Photo')),
        ('video', _('Video')),
        ('audio', _('Audio')),
    ]
    
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='media_assets')
    uploader = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    asset_type = models.CharField(_('asset type'), max_length=20, choices=ASSET_TYPES)
    
    # File storage
    file_path = models.URLField(_('file path'), max_length=500)  # S3/storage URL
    file_hash = models.CharField(_('file hash (SHA256)'), max_length=64, db_index=True)
    file_size = models.BigIntegerField(_('file size (bytes)'))
    mime_type = models.CharField(_('MIME type'), max_length=100)
    thumbnail_path = models.URLField(_('thumbnail path'), max_length=500, blank=True)
    
    # Metadata
    original_filename = models.CharField(_('original filename'), max_length=255)
    compression_applied = models.BooleanField(_('compression applied'), default=False)
    exif_scrubbed = models.BooleanField(_('EXIF scrubbed'), default=False)
    geotag_removed = models.BooleanField(_('geotag removed'), default=False)
    
    # Privacy
    faces_redacted = models.BooleanField(_('faces redacted'), default=False)
    license_plates_redacted = models.BooleanField(_('license plates redacted'), default=False)
    redaction_config = JSONField(_('redaction config'), default=dict, blank=True)
    
    # Security
    virus_scan_status = models.CharField(_('virus scan status'), max_length=20, default='pending',
                                        choices=[('pending', 'Pending'), ('clean', 'Clean'), ('infected', 'Infected')])
    virus_scan_result = models.TextField(_('virus scan result'), blank=True)
    
    # Blockchain
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    blockchain_tx_hash = models.CharField(_('blockchain transaction hash'), max_length=66, null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'media_assets'
        verbose_name = _('media asset')
        verbose_name_plural = _('media assets')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.asset_type} - {self.incident.incident_id}"

