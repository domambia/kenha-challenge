"""
Verification and AI views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import AIVerificationResult, HumanReview
from .serializers import AIVerificationResultSerializer, HumanReviewSerializer
from apps.incidents.models import Incident


class AIVerificationResultViewSet(viewsets.ReadOnlyModelViewSet):
    """AI verification results"""
    queryset = AIVerificationResult.objects.all()
    serializer_class = AIVerificationResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        incident_id = self.request.query_params.get('incident_id', None)
        if incident_id:
            queryset = queryset.filter(incident__incident_id=incident_id)
        return queryset


class HumanReviewViewSet(viewsets.ModelViewSet):
    """Human review management"""
    queryset = HumanReview.objects.all()
    serializer_class = HumanReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def queue(self, request):
        """Get review queue for current user"""
        user_role = request.user.role
        
        # Filter based on user role
        queryset = self.queryset.filter(review_status='pending')
        
        # TODO: Add role-based filtering logic
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
