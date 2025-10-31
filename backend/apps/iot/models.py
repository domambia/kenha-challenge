"""
IoT integration models for KeNHA systems (RFID, CCTV, Sensors)
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField


class RFIDReader(models.Model):
    """RFID reader configuration and metadata"""
    reader_id = models.CharField(_('reader ID'), max_length=100, unique=True, db_index=True)
    
    # Location (PostGIS PointField ready)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    
    # Metadata
    installation_date = models.DateTimeField(_('installation date'), null=True, blank=True)
    manufacturer = models.CharField(_('manufacturer'), max_length=100, blank=True)
    model = models.CharField(_('model'), max_length=100, blank=True)
    
    # Integration
    api_endpoint = models.URLField(_('API endpoint'), max_length=500, blank=True)
    mqtt_topic = models.CharField(_('MQTT topic'), max_length=200, blank=True)
    
    # Status
    status = models.CharField(_('status'), max_length=20, choices=[
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('maintenance', _('Maintenance')),
    ], default='active')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'rfid_readers'
        verbose_name = _('RFID reader')
        verbose_name_plural = _('RFID readers')
        ordering = ['reader_id']
    
    def __str__(self):
        return f"RFID Reader {self.reader_id}"


class RFIDLog(models.Model):
    """RFID reading logs - time-series data for vehicle tracking"""
    reader = models.ForeignKey(RFIDReader, on_delete=models.CASCADE, related_name='readings')
    
    # Vehicle data (privacy-preserved)
    vehicle_tag = models.CharField(_('vehicle tag (hashed)'), max_length=255, db_index=True)
    vehicle_registration = models.CharField(_('vehicle registration (hashed)'), max_length=255, blank=True)
    
    # Temporal data
    timestamp = models.DateTimeField(_('timestamp'), db_index=True)
    
    # Spatial data
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Metadata
    direction = models.CharField(_('direction'), max_length=20, blank=True)
    lane = models.IntegerField(_('lane number'), null=True, blank=True)
    speed = models.DecimalField(_('speed (km/h)'), max_digits=5, decimal_places=2, null=True, blank=True)
    vehicle_type = models.CharField(_('vehicle type'), max_length=50, blank=True)
    vehicle_class = models.CharField(_('vehicle class'), max_length=20, blank=True)
    
    # Blockchain hash for audit trail
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'rfid_logs'
        verbose_name = _('RFID log')
        verbose_name_plural = _('RFID logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'reader']),
            models.Index(fields=['vehicle_tag', 'timestamp']),
        ]
    
    def __str__(self):
        return f"RFID Log {self.reader.reader_id} @ {self.timestamp}"


class CCTVCamera(models.Model):
    """CCTV camera configuration for KeNHA surveillance network"""
    camera_id = models.CharField(_('camera ID'), max_length=100, unique=True, db_index=True)
    
    # Location (PostGIS PointField ready)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    
    # Coverage
    coverage_radius_meters = models.IntegerField(_('coverage radius (meters)'), default=500)
    
    # Installation
    installation_date = models.DateTimeField(_('installation date'), null=True, blank=True)
    camera_type = models.CharField(_('camera type'), max_length=50, blank=True)
    
    # Protocol & Connection
    protocol = models.CharField(_('protocol'), max_length=20, choices=[
        ('RTSP', 'RTSP'),
        ('ONVIF', 'ONVIF'),
        ('proprietary', _('Proprietary')),
    ], default='RTSP')
    
    api_endpoint = models.URLField(_('API endpoint'), max_length=500, blank=True)
    rtsp_url = models.URLField(_('RTSP URL'), max_length=500, blank=True)
    onvif_url = models.URLField(_('ONVIF URL'), max_length=500, blank=True)
    
    # Metadata
    metadata = JSONField(_('metadata'), default=dict, blank=True)
    
    # Status
    status = models.CharField(_('status'), max_length=20, choices=[
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('maintenance', _('Maintenance')),
    ], default='active')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'cctv_cameras'
        verbose_name = _('CCTV camera')
        verbose_name_plural = _('CCTV cameras')
        ordering = ['camera_id']
    
    def __str__(self):
        return f"CCTV Camera {self.camera_id}"


class CCTVFeed(models.Model):
    """CCTV feed retrieval and analysis results"""
    camera = models.ForeignKey(CCTVCamera, on_delete=models.CASCADE, related_name='feeds')
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, null=True, blank=True, related_name='cctv_feeds')
    
    # Time window
    start_time = models.DateTimeField(_('start time'), db_index=True)
    end_time = models.DateTimeField(_('end time'))
    
    # Video storage
    video_file_path = models.URLField(_('video file path'), max_length=500, blank=True)
    
    # AI Analysis
    ai_analysis_result = JSONField(_('AI analysis result'), default=dict, blank=True)
    incident_detected = models.BooleanField(_('incident detected'), default=False)
    confidence_score = models.DecimalField(_('confidence score'), max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Review
    manual_review_status = models.CharField(_('manual review status'), max_length=20, choices=[
        ('pending', _('Pending')),
        ('reviewed', _('Reviewed')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ], default='pending')
    reviewed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(_('reviewed at'), null=True, blank=True)
    
    # Blockchain & Retention
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    retention_until = models.DateTimeField(_('retention until'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'cctv_feeds'
        verbose_name = _('CCTV feed')
        verbose_name_plural = _('CCTV feeds')
        ordering = ['-start_time']
    
    def __str__(self):
        return f"CCTV Feed {self.camera.camera_id} @ {self.start_time}"


class Sensor(models.Model):
    """Sensor configuration for KeNHA sensor network"""
    SENSOR_TYPES = [
        ('traffic_flow', _('Traffic Flow')),
        ('weather', _('Weather')),
        ('road_surface', _('Road Surface')),
        ('air_quality', _('Air Quality')),
        ('vibration', _('Vibration')),
    ]
    
    sensor_id = models.CharField(_('sensor ID'), max_length=100, unique=True, db_index=True)
    
    # Location (PostGIS PointField ready)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    
    # Type
    sensor_type = models.CharField(_('sensor type'), max_length=50, choices=SENSOR_TYPES)
    
    # Installation
    installation_date = models.DateTimeField(_('installation date'), null=True, blank=True)
    manufacturer = models.CharField(_('manufacturer'), max_length=100, blank=True)
    model = models.CharField(_('model'), max_length=100, blank=True)
    
    # Integration
    api_endpoint = models.URLField(_('API endpoint'), max_length=500, blank=True)
    mqtt_topic = models.CharField(_('MQTT topic'), max_length=200, blank=True)
    
    # Metadata
    metadata = JSONField(_('metadata'), default=dict, blank=True)
    
    # Status
    status = models.CharField(_('status'), max_length=20, choices=[
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('maintenance', _('Maintenance')),
    ], default='active')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        db_table = 'sensors'
        verbose_name = _('sensor')
        verbose_name_plural = _('sensors')
        ordering = ['sensor_type', 'sensor_id']
    
    def __str__(self):
        return f"{self.get_sensor_type_display()} Sensor {self.sensor_id}"


class SensorReading(models.Model):
    """Sensor readings - time-series data"""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    
    # Temporal data
    timestamp = models.DateTimeField(_('timestamp'), db_index=True)
    
    # Reading data (flexible JSON schema per sensor type)
    reading_type = models.CharField(_('reading type'), max_length=50)
    value = JSONField(_('value'), default=dict)  # Can store different types of readings
    unit = models.CharField(_('unit'), max_length=20, blank=True)
    
    # Quality
    quality_score = models.DecimalField(_('quality score'), max_digits=5, decimal_places=2, null=True, blank=True)
    anomaly_detected = models.BooleanField(_('anomaly detected'), default=False)
    
    # Blockchain hash for critical readings
    blockchain_hash = models.CharField(_('blockchain hash'), max_length=66, null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        db_table = 'sensor_readings'
        verbose_name = _('sensor reading')
        verbose_name_plural = _('sensor readings')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'sensor']),
            models.Index(fields=['sensor', 'anomaly_detected']),
        ]
    
    def __str__(self):
        return f"{self.sensor.sensor_id} Reading @ {self.timestamp}"


class IncidentValidation(models.Model):
    """Multi-source validation results for incidents"""
    VALIDATION_SOURCES = [
        ('citizen_report', _('Citizen Report')),
        ('rfid', _('RFID')),
        ('cctv', _('CCTV')),
        ('sensor', _('Sensor')),
        ('ai', _('AI Analysis')),
    ]
    
    VALIDATION_STATUSES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('contradicted', _('Contradicted')),
        ('inconclusive', _('Inconclusive')),
    ]
    
    incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name='validations')
    validation_source = models.CharField(_('validation source'), max_length=20, choices=VALIDATION_SOURCES)
    
    # Confidence & Status
    confidence_score = models.DecimalField(_('confidence score'), max_digits=5, decimal_places=2,
                                          help_text=_('0-100% confidence'))
    validation_status = models.CharField(_('validation status'), max_length=20, choices=VALIDATION_STATUSES,
                                        default='pending')
    
    # Source data & correlation details
    source_data = JSONField(_('source data'), default=dict, blank=True)
    correlation_details = JSONField(_('correlation details'), default=dict, blank=True)
    
    # Metadata
    validated_at = models.DateTimeField(_('validated at'), auto_now_add=True)
    validated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='validated_incidents')
    
    class Meta:
        db_table = 'incident_validations'
        verbose_name = _('incident validation')
        verbose_name_plural = _('incident validations')
        ordering = ['-validated_at']
        unique_together = [['incident', 'validation_source']]
    
    def __str__(self):
        return f"{self.incident.incident_id} - {self.get_validation_source_display()} ({self.confidence_score}%)"
