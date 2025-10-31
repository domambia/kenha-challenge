"""
Analytics views
"""
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg

from apps.incidents.models import Incident
from apps.response.models import IncidentAssignment
from apps.iot.models import (
    Sensor, SensorReading, RFIDReader, RFIDLog,
    CCTVCamera, CCTVFeed
)


class AnalyticsDashboardView(views.APIView):
    """Analytics dashboard data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get dashboard analytics"""
        # Time range (last 30 days)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Incident statistics
        total_incidents = Incident.objects.filter(
            created_at__gte=start_date
        ).count()
        
        resolved_incidents = Incident.objects.filter(
            status='resolved',
            created_at__gte=start_date
        ).count()
        
        avg_response_time = self._calculate_avg_response_time(start_date, end_date)
        
        # Get IoT device status
        iot_status = self._get_iot_status()
        
        # Get traffic flow summary
        traffic_summary = self._get_traffic_summary(start_date, end_date)
        
        return Response({
            'total_incidents': total_incidents,
            'resolved_incidents': resolved_incidents,
            'avg_response_time_minutes': avg_response_time,
            'active_incidents': total_incidents - resolved_incidents,
            'iot_status': iot_status,
            'traffic_summary': traffic_summary,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
            }
        })
    
    def _calculate_avg_response_time(self, start_date, end_date):
        """Calculate average response time in minutes"""
        assignments = IncidentAssignment.objects.filter(
            assigned_at__gte=start_date,
            assigned_at__lte=end_date,
            accepted_at__isnull=False
        )
        
        if not assignments.exists():
            return 0
        
        total_time = 0
        count = 0
        for assignment in assignments:
            if assignment.accepted_at and assignment.assigned_at:
                delta = assignment.accepted_at - assignment.assigned_at
                total_time += delta.total_seconds() / 60
                count += 1
        
        return round(total_time / count, 2) if count > 0 else 0
    
    def _get_iot_status(self):
        """Get IoT device status summary"""
        # CCTV cameras
        cctv_total = CCTVCamera.objects.count()
        cctv_online = CCTVCamera.objects.filter(status='active').count()
        
        # RFID readers
        rfid_total = RFIDReader.objects.count()
        rfid_online = RFIDReader.objects.filter(status='active').count()
        
        # Traffic sensors
        traffic_sensors_total = Sensor.objects.filter(sensor_type='traffic_flow').count()
        traffic_sensors_online = Sensor.objects.filter(
            sensor_type='traffic_flow',
            status='active'
        ).count()
        
        # All sensors (for general count)
        all_sensors_total = Sensor.objects.count()
        all_sensors_online = Sensor.objects.filter(status='active').count()
        
        # Active responders (from assignments)
        active_responders = IncidentAssignment.objects.filter(
            status__in=['assigned', 'in_progress']
        ).values('assigned_to').distinct().count()
        
        return {
            'cctv_cameras': {
                'total': cctv_total,
                'online': cctv_online,
                'offline': cctv_total - cctv_online
            },
            'rfid_readers': {
                'total': rfid_total,
                'online': rfid_online,
                'offline': rfid_total - rfid_online
            },
            'traffic_sensors': {
                'total': traffic_sensors_total,
                'online': traffic_sensors_online,
                'offline': traffic_sensors_total - traffic_sensors_online
            },
            'all_sensors': {
                'total': all_sensors_total,
                'online': all_sensors_online,
                'offline': all_sensors_total - all_sensors_online
            },
            'active_responders': active_responders
        }
    
    def _get_traffic_summary(self, start_date, end_date):
        """Get traffic flow summary from RFID logs and traffic sensors"""
        # Get recent RFID logs (last 24 hours)
        recent_date = timezone.now() - timedelta(hours=24)
        
        # RFID traffic data
        rfid_logs = RFIDLog.objects.filter(timestamp__gte=recent_date)
        total_vehicles = rfid_logs.count()
        
        avg_speed = None
        if rfid_logs.filter(speed__isnull=False).exists():
            avg_speed_result = rfid_logs.filter(speed__isnull=False).aggregate(
                avg_speed=Avg('speed')
            )
            avg_speed = float(avg_speed_result['avg_speed']) if avg_speed_result['avg_speed'] else None
        
        # Traffic flow sensor readings
        traffic_sensors = Sensor.objects.filter(sensor_type='traffic_flow', status='active')
        traffic_readings = SensorReading.objects.filter(
            sensor__in=traffic_sensors,
            timestamp__gte=recent_date,
            reading_type__in=['vehicle_count', 'speed', 'occupancy']
        )
        
        # Aggregate traffic data
        vehicle_counts = []
        avg_speeds = []
        
        for reading in traffic_readings:
            value_data = reading.value if isinstance(reading.value, dict) else {}
            if reading.reading_type == 'vehicle_count':
                count = value_data.get('count', value_data.get('value', 0))
                if isinstance(count, (int, float)):
                    vehicle_counts.append(count)
            elif reading.reading_type == 'speed':
                speed = value_data.get('speed', value_data.get('value', 0))
                if isinstance(speed, (int, float)) and speed > 0:
                    avg_speeds.append(speed)
        
        avg_vehicle_count = sum(vehicle_counts) / len(vehicle_counts) if vehicle_counts else 0
        avg_traffic_speed = sum(avg_speeds) / len(avg_speeds) if avg_speeds else None
        
        # Combine RFID and sensor data
        if avg_traffic_speed is None and avg_speed:
            avg_traffic_speed = avg_speed
        
        return {
            'total_vehicles_24h': total_vehicles,
            'avg_speed_kmh': round(avg_traffic_speed, 1) if avg_traffic_speed else None,
            'avg_vehicle_count': round(avg_vehicle_count, 1) if vehicle_counts else None,
            'period_hours': 24
        }


class IncidentHeatmapView(views.APIView):
    """Incident heatmap data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get incident heatmap coordinates"""
        incidents = Incident.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).values('latitude', 'longitude', 'severity__level')[:1000]
        
        return Response({
            'incidents': list(incidents)
        })


class TrafficFlowView(views.APIView):
    """Traffic flow analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get traffic flow data"""
        hours = int(request.query_params.get('hours', 24))
        recent_date = timezone.now() - timedelta(hours=hours)
        
        # RFID logs
        rfid_logs = RFIDLog.objects.filter(timestamp__gte=recent_date)
        
        # Traffic sensor readings
        traffic_sensors = Sensor.objects.filter(sensor_type='traffic_flow', status='active')
        traffic_readings = SensorReading.objects.filter(
            sensor__in=traffic_sensors,
            timestamp__gte=recent_date
        ).order_by('-timestamp')
        
        # Aggregate by hour
        hourly_data = {}
        for reading in traffic_readings[:100]:  # Limit for performance
            hour_key = reading.timestamp.replace(minute=0, second=0, microsecond=0).isoformat()
            if hour_key not in hourly_data:
                hourly_data[hour_key] = {'vehicle_count': 0, 'speed': [], 'count': 0}
            
            value_data = reading.value if isinstance(reading.value, dict) else {}
            if reading.reading_type == 'vehicle_count':
                count = value_data.get('count', value_data.get('value', 0))
                if isinstance(count, (int, float)):
                    hourly_data[hour_key]['vehicle_count'] += count
                    hourly_data[hour_key]['count'] += 1
            elif reading.reading_type == 'speed':
                speed = value_data.get('speed', value_data.get('value', 0))
                if isinstance(speed, (int, float)) and speed > 0:
                    hourly_data[hour_key]['speed'].append(speed)
        
        # Format hourly data
        traffic_timeline = []
        for hour, data in sorted(hourly_data.items()):
            avg_speed = sum(data['speed']) / len(data['speed']) if data['speed'] else None
            traffic_timeline.append({
                'timestamp': hour,
                'vehicle_count': data['vehicle_count'],
                'avg_speed': round(avg_speed, 1) if avg_speed else None
            })
        
        return Response({
            'total_vehicles': rfid_logs.count(),
            'timeline': traffic_timeline,
            'period_hours': hours
        })


class WeatherConditionsView(views.APIView):
    """Weather conditions from sensors"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current weather conditions"""
        # Get latest weather sensor readings
        weather_sensors = Sensor.objects.filter(sensor_type='weather', status='active')
        latest_readings = SensorReading.objects.filter(
            sensor__in=weather_sensors
        ).order_by('-timestamp')[:50]
        
        weather_data = {}
        for reading in latest_readings:
            sensor_id = reading.sensor.sensor_id
            if sensor_id not in weather_data:
                value_data = reading.value if isinstance(reading.value, dict) else {}
                weather_data[sensor_id] = {
                    'sensor_id': sensor_id,
                    'location': {
                        'latitude': float(reading.sensor.latitude),
                        'longitude': float(reading.sensor.longitude)
                    },
                    'temperature': value_data.get('temperature'),
                    'humidity': value_data.get('humidity'),
                    'rainfall': value_data.get('rainfall'),
                    'wind_speed': value_data.get('wind_speed'),
                    'visibility': value_data.get('visibility'),
                    'timestamp': reading.timestamp.isoformat()
                }
        
        return Response({
            'conditions': list(weather_data.values()),
            'total_sensors': weather_sensors.count()
        })


class RoadConditionsView(views.APIView):
    """Road surface conditions from sensors"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get road surface conditions"""
        # Get latest road surface sensor readings
        road_sensors = Sensor.objects.filter(sensor_type='road_surface', status='active')
        latest_readings = SensorReading.objects.filter(
            sensor__in=road_sensors
        ).order_by('-timestamp')[:50]
        
        road_data = {}
        for reading in latest_readings:
            sensor_id = reading.sensor.sensor_id
            if sensor_id not in road_data:
                value_data = reading.value if isinstance(reading.value, dict) else {}
                road_data[sensor_id] = {
                    'sensor_id': sensor_id,
                    'location': {
                        'latitude': float(reading.sensor.latitude),
                        'longitude': float(reading.sensor.longitude)
                    },
                    'condition': value_data.get('condition', 'unknown'),  # dry, wet, icy, etc.
                    'temperature': value_data.get('temperature'),
                    'surface_type': value_data.get('surface_type'),
                    'roughness': value_data.get('roughness'),
                    'anomaly_detected': reading.anomaly_detected,
                    'timestamp': reading.timestamp.isoformat()
                }
        
        return Response({
            'conditions': list(road_data.values()),
            'total_sensors': road_sensors.count()
        })
