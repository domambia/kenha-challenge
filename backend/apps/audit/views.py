"""
Audit log views
"""
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit log queries (read-only)"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO: Add admin permission check
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by entity if provided
        entity_type = self.request.query_params.get('entity_type', None)
        entity_id = self.request.query_params.get('entity_id', None)
        
        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        if entity_id:
            queryset = queryset.filter(entity_id=entity_id)
        
        return queryset
