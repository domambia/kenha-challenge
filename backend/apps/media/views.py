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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Get incident
        incident_id = request.data.get('incident_id')
        if not incident_id:
            return Response(
                {'error': 'incident_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        incident = get_object_or_404(Incident, incident_id=incident_id)
        
        # Add incident to validated data
        serializer.validated_data['incident'] = incident
        
        # Set uploader if authenticated
        if request.user and request.user.is_authenticated:
            serializer.validated_data['uploader'] = request.user
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
