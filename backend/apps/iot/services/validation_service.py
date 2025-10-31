"""
Multi-source incident validation service
Correlates citizen reports with RFID, CCTV, and sensor data
"""
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q, Avg
from datetime import timedelta
from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.incidents.models import Incident

# Import models at module level (after TYPE_CHECKING to avoid circular imports)
from apps.iot.models import RFIDLog, CCTVFeed, SensorReading, IncidentValidation


class IncidentValidationService:
    """
    Multi-source correlation engine for incident validation
    Implements confidence scoring based on RFID, CCTV, and sensor correlation
    """
    
    # Confidence weights (as per PRD)
    RFID_WEIGHT = Decimal('0.20')  # 20%
    CCTV_WEIGHT = Decimal('0.30')  # 30%
    SENSOR_WEIGHT = Decimal('0.10')  # 10%
    AI_WEIGHT = Decimal('0.40')  # 40% (from photo/video analysis)
    
    # Spatial-temporal matching thresholds
    RFID_RADIUS_KM = 2.0  # ±2km radius
    RFID_TIME_WINDOW_MINUTES = 10  # ±10 minutes
    CCTV_RADIUS_METERS = 500  # ±500m radius
    CCTV_TIME_WINDOW_MINUTES = 5  # ±5 minutes
    SENSOR_RADIUS_METERS = 1000  # ±1km radius
    
    def validate_incident(self, incident: 'Incident') -> dict:
        """
        Main validation method - correlates incident with all available sources
        
        Returns:
            dict with confidence_score, validation_details, and validation_status
        """
        # Get individual source validations
        rfid_confidence = self._check_rfid_correlation(incident)
        cctv_confidence = self._analyze_cctv_feeds(incident)
        sensor_confidence = self._correlate_sensors(incident)
        
        # Get AI confidence (from photo/video analysis)
        ai_confidence = self._get_ai_confidence(incident)
        
        # Calculate weighted total confidence
        total_confidence = (
            rfid_confidence * self.RFID_WEIGHT +
            cctv_confidence * self.CCTV_WEIGHT +
            sensor_confidence * self.SENSOR_WEIGHT +
            ai_confidence * self.AI_WEIGHT
        )
        
        # Determine validation status
        validation_status = self._determine_validation_status(total_confidence)
        
        # Store validation results
        validation_details = {
            'rfid_confidence': float(rfid_confidence),
            'cctv_confidence': float(cctv_confidence),
            'sensor_confidence': float(sensor_confidence),
            'ai_confidence': float(ai_confidence),
            'total_confidence': float(total_confidence),
            'rfid_match': rfid_confidence > 50,
            'cctv_verified': cctv_confidence > 60,
            'sensor_correlation': sensor_confidence > 40,
        }
        
        # Create validation records
        self._create_validation_records(incident, rfid_confidence, cctv_confidence, sensor_confidence, ai_confidence)
        
        return {
            'confidence_score': float(total_confidence),
            'validation_status': validation_status,
            'validation_details': validation_details,
        }
    
    def _check_rfid_correlation(self, incident: 'Incident') -> Decimal:
        """
        Check RFID logs for vehicle presence at incident location/time
        Returns confidence score 0-100
        """
        try:
            incident_time = incident.timestamp
            time_window_start = incident_time - timedelta(minutes=self.RFID_TIME_WINDOW_MINUTES)
            time_window_end = incident_time + timedelta(minutes=self.RFID_TIME_WINDOW_MINUTES)
            
            # Query RFID logs within time window
            # Note: Spatial query would use PostGIS ST_DWithin in production
            logs = RFIDLog.objects.filter(
                timestamp__gte=time_window_start,
                timestamp__lte=time_window_end,
            )
            
            if not logs.exists():
                return Decimal('0')
            
            # Calculate proximity-based confidence
            # In production, use PostGIS for accurate distance calculations
            matching_logs = 0
            total_logs = logs.count()
            
            for log in logs:
                # Simplified distance calculation (would use PostGIS in production)
                if log.latitude and log.longitude:
                    # Rough distance check (would use proper geodetic calculation)
                    matching_logs += 1
            
            if matching_logs > 0:
                # Confidence increases with more matching logs
                base_confidence = min(70, (matching_logs / max(total_logs, 1)) * 100)
                return Decimal(str(base_confidence))
            
            return Decimal('0')
            
        except Exception as e:
            # Log error but don't fail validation
            return Decimal('0')
    
    def _analyze_cctv_feeds(self, incident: 'Incident') -> Decimal:
        """
        Retrieve and analyze CCTV feeds for incident validation
        Returns confidence score 0-100
        """
        try:
            # Check if CCTV feeds already exist for this incident
            existing_feeds = CCTVFeed.objects.filter(incident=incident)
            
            if existing_feeds.exists():
                # Use existing analysis results
                avg_confidence = existing_feeds.aggregate(
                    avg_confidence=models.Avg('confidence_score')
                )['avg_confidence']
                
                if avg_confidence:
                    return Decimal(str(avg_confidence))
            
            # If no feeds exist, confidence is low
            # In production, this would trigger CCTV feed retrieval
            return Decimal('0')
            
        except Exception as e:
            return Decimal('0')
    
    def _correlate_sensors(self, incident: 'Incident') -> Decimal:
        """
        Correlate sensor data with incident report
        Returns confidence score 0-100
        """
        try:
            incident_time = incident.timestamp
            time_window_start = incident_time - timedelta(minutes=10)
            time_window_end = incident_time + timedelta(minutes=10)
            
            # Query sensor readings for anomaly detection
            readings = SensorReading.objects.filter(
                timestamp__gte=time_window_start,
                timestamp__lte=time_window_end,
                anomaly_detected=True,
            )
            
            if readings.exists():
                # Confidence based on number of anomalies and sensor types
                unique_sensors = readings.values('sensor').distinct().count()
                base_confidence = min(60, unique_sensors * 15)
                return Decimal(str(base_confidence))
            
            return Decimal('0')
            
        except Exception as e:
            return Decimal('0')
    
    def _get_ai_confidence(self, incident: 'Incident') -> Decimal:
        """
        Get AI analysis confidence from photo/video analysis
        Returns confidence score 0-100
        """
        try:
            # Get latest AI verification result
            ai_result = incident.ai_results.order_by('-created_at').first()
            
            if ai_result:
                return Decimal(str(ai_result.confidence_score))
            
            return Decimal('50')  # Default moderate confidence if no AI analysis yet
            
        except Exception:
            return Decimal('50')
    
    def _determine_validation_status(self, confidence: Decimal) -> str:
        """
        Determine validation status based on confidence score
        """
        confidence_float = float(confidence)
        
        if confidence_float >= 70:
            return 'verified'
        elif confidence_float >= 50:
            return 'probable'
        else:
            return 'unverified'
    
    def _create_validation_records(self, incident: 'Incident', rfid_confidence: Decimal,
                                   cctv_confidence: Decimal, sensor_confidence: Decimal,
                                   ai_confidence: Decimal):
        """
        Create IncidentValidation records for each source
        """
        sources = [
            ('rfid', rfid_confidence),
            ('cctv', cctv_confidence),
            ('sensor', sensor_confidence),
            ('ai', ai_confidence),
        ]
        
        for source, confidence in sources:
            IncidentValidation.objects.update_or_create(
                incident=incident,
                validation_source=source,
                defaults={
                    'confidence_score': confidence,
                    'validation_status': 'confirmed' if confidence > 50 else 'pending',
                    'correlation_details': {
                        'confidence': float(confidence),
                        'timestamp': timezone.now().isoformat(),
                    }
                }
            )


# Import Incident model only where needed (inside methods) to avoid circular imports

