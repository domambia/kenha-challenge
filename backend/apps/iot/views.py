"""
IoT integration views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    RFIDReader, RFIDLog, CCTVCamera, CCTVFeed,
    Sensor, SensorReading, IncidentValidation
)
from .serializers import (
    RFIDReaderSerializer, RFIDLogSerializer, CCTVCameraSerializer,
    CCTVFeedSerializer, SensorSerializer, SensorReadingSerializer,
    IncidentValidationSerializer
)
from apps.incidents.models import Incident
from .services.validation_service import IncidentValidationService


class RFIDReaderViewSet(viewsets.ModelViewSet):
    """RFID reader management"""
    queryset = RFIDReader.objects.all()
    serializer_class = RFIDReaderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'reader_id'


class RFIDLogViewSet(viewsets.ReadOnlyModelViewSet):
    """RFID log queries"""
    queryset = RFIDLog.objects.all()
    serializer_class = RFIDLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering
        reader_id = self.request.query_params.get('reader_id', None)
        if reader_id:
            queryset = queryset.filter(reader__reader_id=reader_id)
        return queryset


class CCTVCameraViewSet(viewsets.ModelViewSet):
    """CCTV camera management"""
    queryset = CCTVCamera.objects.all()
    serializer_class = CCTVCameraSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'camera_id'


class CCTVFeedViewSet(viewsets.ModelViewSet):
    """CCTV feed management"""
    queryset = CCTVFeed.objects.all()
    serializer_class = CCTVFeedSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def retrieve_for_incident(self, request):
        """Retrieve CCTV feeds for a specific incident"""
        incident_id = request.data.get('incident_id')
        incident = get_object_or_404(Incident, incident_id=incident_id)
        
        # TODO: Implement actual CCTV feed retrieval logic
        return Response({'message': 'CCTV feed retrieval initiated'})


class SensorViewSet(viewsets.ModelViewSet):
    """Sensor management"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'sensor_id'


class SensorReadingViewSet(viewsets.ReadOnlyModelViewSet):
    """Sensor reading queries"""
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sensor_id = self.request.query_params.get('sensor_id', None)
        if sensor_id:
            queryset = queryset.filter(sensor__sensor_id=sensor_id)
        return queryset


class IncidentValidationViewSet(viewsets.ModelViewSet):
    """Incident validation management"""
    queryset = IncidentValidation.objects.all()
    serializer_class = IncidentValidationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def validate_incident(self, request):
        """Trigger multi-source validation for an incident"""
        incident_id = request.data.get('incident_id')
        incident = get_object_or_404(Incident, incident_id=incident_id)
        
        # Run validation service
        service = IncidentValidationService()
        result = service.validate_incident(incident)
        
        # Update incident with validation results
        incident.verification_status = result['validation_status']
        incident.ai_confidence_score = result['confidence_score']
        incident.save()
        
        return Response(result, status=status.HTTP_200_OK)
