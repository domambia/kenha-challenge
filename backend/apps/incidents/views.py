"""
Incident views
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Incident, IncidentComment
from .serializers import IncidentSerializer, IncidentCommentSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """Incident CRUD and operations"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'incident_id'
    
    def get_permissions(self):
        """Allow anonymous users to create incidents"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering based on user role and permissions
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    def perform_create(self, serializer):
        """Handle anonymous reporting"""
        if self.request.user.is_authenticated:
            serializer.save(reporter=self.request.user, is_anonymous=False)
        else:
            serializer.save(is_anonymous=True)
    
    @action(detail=True, methods=['patch'])
    def verify(self, request, incident_id=None):
        """Verify incident (dispatcher/QA)"""
        incident = self.get_object()
        # TODO: Implement verification logic
        incident.verification_status = 'verified'
        incident.save()
        return Response({'message': 'Incident verified'})
    
    @action(detail=True, methods=['patch'])
    def assign(self, request, incident_id=None):
        """Assign incident to responder"""
        incident = self.get_object()
        # TODO: Implement assignment logic
        return Response({'message': 'Incident assigned'})
    
    @action(detail=True, methods=['patch'])
    def close(self, request, incident_id=None):
        """Close incident with resolution notes"""
        incident = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        incident.status = 'closed'
        incident.resolution_notes = resolution_notes
        incident.save()
        return Response({'message': 'Incident closed'})


class IncidentCommentViewSet(viewsets.ModelViewSet):
    """Comments on incidents"""
    queryset = IncidentComment.objects.all()
    serializer_class = IncidentCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        incident_id = self.request.query_params.get('incident_id', None)
        if incident_id:
            queryset = queryset.filter(incident__incident_id=incident_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
