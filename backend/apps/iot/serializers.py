"""
IoT integration serializers
"""
from rest_framework import serializers
from .models import (
    RFIDReader, RFIDLog, CCTVCamera, CCTVFeed,
    Sensor, SensorReading, IncidentValidation
)


class RFIDReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDReader
        fields = ['id', 'reader_id', 'latitude', 'longitude', 'status', 
                 'manufacturer', 'model', 'installation_date']
        read_only_fields = ['id']


class RFIDLogSerializer(serializers.ModelSerializer):
    reader_id = serializers.CharField(source='reader.reader_id', read_only=True)
    
    class Meta:
        model = RFIDLog
        fields = ['id', 'reader_id', 'vehicle_tag', 'timestamp', 'direction',
                 'lane', 'speed', 'vehicle_type', 'latitude', 'longitude']
        read_only_fields = ['id']


class CCTVCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTVCamera
        fields = ['id', 'camera_id', 'latitude', 'longitude', 'protocol',
                 'coverage_radius_meters', 'status', 'rtsp_url']
        read_only_fields = ['id']


class CCTVFeedSerializer(serializers.ModelSerializer):
    camera_id = serializers.CharField(source='camera.camera_id', read_only=True)
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    
    class Meta:
        model = CCTVFeed
        fields = ['id', 'camera_id', 'incident_id', 'start_time', 'end_time',
                 'video_file_path', 'incident_detected', 'confidence_score',
                 'manual_review_status']
        read_only_fields = ['id']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'sensor_id', 'sensor_type', 'latitude', 'longitude',
                 'status', 'manufacturer', 'model']
        read_only_fields = ['id']


class SensorReadingSerializer(serializers.ModelSerializer):
    sensor_id = serializers.CharField(source='sensor.sensor_id', read_only=True)
    
    class Meta:
        model = SensorReading
        fields = ['id', 'sensor_id', 'timestamp', 'reading_type', 'value',
                 'unit', 'anomaly_detected', 'quality_score']
        read_only_fields = ['id']


class IncidentValidationSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    
    class Meta:
        model = IncidentValidation
        fields = ['id', 'incident_id', 'validation_source', 'confidence_score',
                 'validation_status', 'correlation_details', 'validated_at']
        read_only_fields = ['id', 'validated_at']
