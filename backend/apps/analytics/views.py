"""
Analytics views
"""
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count, Q

from apps.incidents.models import Incident
from apps.response.models import IncidentAssignment


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
        
        return Response({
            'total_incidents': total_incidents,
            'resolved_incidents': resolved_incidents,
            'avg_response_time_minutes': avg_response_time,
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
