from django.contrib import admin
from .models import RFIDReader, RFIDLog, CCTVCamera, CCTVFeed, Sensor, SensorReading, IncidentValidation


@admin.register(RFIDReader)
class RFIDReaderAdmin(admin.ModelAdmin):
    list_display = ['reader_id', 'status', 'latitude', 'longitude', 'installation_date']
    list_filter = ['status', 'installation_date']
    search_fields = ['reader_id', 'manufacturer', 'model']


@admin.register(RFIDLog)
class RFIDLogAdmin(admin.ModelAdmin):
    list_display = ['reader', 'vehicle_tag', 'timestamp', 'direction', 'speed']
    list_filter = ['timestamp', 'reader']
    search_fields = ['vehicle_tag', 'vehicle_registration']
    date_hierarchy = 'timestamp'


@admin.register(CCTVCamera)
class CCTVCameraAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'protocol', 'status', 'coverage_radius_meters', 'latitude', 'longitude']
    list_filter = ['status', 'protocol']
    search_fields = ['camera_id', 'camera_type']


@admin.register(CCTVFeed)
class CCTVFeedAdmin(admin.ModelAdmin):
    list_display = ['camera', 'incident', 'start_time', 'incident_detected', 'confidence_score', 'manual_review_status']
    list_filter = ['manual_review_status', 'incident_detected', 'start_time']
    search_fields = ['camera__camera_id']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['sensor_id', 'sensor_type', 'status', 'latitude', 'longitude']
    list_filter = ['sensor_type', 'status']
    search_fields = ['sensor_id', 'manufacturer', 'model']


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'timestamp', 'reading_type', 'anomaly_detected']
    list_filter = ['anomaly_detected', 'reading_type', 'timestamp']
    date_hierarchy = 'timestamp'


@admin.register(IncidentValidation)
class IncidentValidationAdmin(admin.ModelAdmin):
    list_display = ['incident', 'validation_source', 'confidence_score', 'validation_status', 'validated_at']
    list_filter = ['validation_source', 'validation_status', 'validated_at']
    search_fields = ['incident__incident_id']

