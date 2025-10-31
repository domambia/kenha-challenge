"""
Media views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import MediaAsset
from .serializers import MediaAssetSerializer
from apps.incidents.models import Incident


class MediaAssetViewSet(viewsets.ModelViewSet):
    """Media asset management"""
    queryset = MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.AllowAny]  # Allow anonymous uploads
    
    def get_queryset(self):
        queryset = super().get_queryset()
        incident_id = self.request.query_params.get('incident_id', None)
        if incident_id:
            queryset = queryset.filter(incident__incident_id=incident_id)
        return queryset
    
    def perform_create(self, serializer):
        incident_id = self.request.data.get('incident_id')
        if incident_id:
            incident = get_object_or_404(Incident, incident_id=incident_id)
            serializer.save(incident=incident)
