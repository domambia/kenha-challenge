"""
Response coordination views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import IncidentAssignment, ResponseMilestone, ResponderLocation, ResponderChecklist
from .serializers import (
    IncidentAssignmentSerializer, ResponseMilestoneSerializer,
    ResponderLocationSerializer, ResponderChecklistSerializer
)
from apps.incidents.models import Incident


class IncidentAssignmentViewSet(viewsets.ModelViewSet):
    """Incident assignment management"""
    queryset = IncidentAssignment.objects.all()
    serializer_class = IncidentAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        """Accept assignment (responder)"""
        assignment = self.get_object()
        assignment.status = 'accepted'
        assignment.accepted_at = timezone.now()
        assignment.save()
        return Response({'message': 'Assignment accepted'})
    
    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        """Reject assignment (responder)"""
        assignment = self.get_object()
        assignment.status = 'rejected'
        assignment.save()
        return Response({'message': 'Assignment rejected'})
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """Complete assignment"""
        assignment = self.get_object()
        assignment.status = 'completed'
        assignment.completed_at = timezone.now()
        assignment.save()
        return Response({'message': 'Assignment completed'})


class ResponseMilestoneViewSet(viewsets.ModelViewSet):
    """Response milestone tracking"""
    queryset = ResponseMilestone.objects.all()
    serializer_class = ResponseMilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        incident_id = self.request.query_params.get('incident_id', None)
        if incident_id:
            queryset = queryset.filter(incident__incident_id=incident_id)
        return queryset


class ResponderLocationViewSet(viewsets.ModelViewSet):
    """Responder location tracking"""
    queryset = ResponderLocation.objects.all()
    serializer_class = ResponderLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def update_location(self, request):
        """Update responder's current location"""
        responder = request.user
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        # Deactivate previous locations
        ResponderLocation.objects.filter(responder=responder, is_active=True).update(is_active=False)
        
        # Create new location
        location = ResponderLocation.objects.create(
            responder=responder,
            latitude=latitude,
            longitude=longitude,
            accuracy=request.data.get('accuracy'),
            speed=request.data.get('speed'),
            heading=request.data.get('heading'),
            is_active=True
        )
        
        serializer = self.get_serializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponderChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    """Responder checklist queries"""
    queryset = ResponderChecklist.objects.all()
    serializer_class = ResponderChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.utils import timezone
