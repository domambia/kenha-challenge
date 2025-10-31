"""
Work order views
"""
from rest_framework import viewsets, permissions
from .models import WorkOrder, InfrastructureInspection
from .serializers import WorkOrderSerializer, InfrastructureInspectionSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
    """Work order management"""
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class InfrastructureInspectionViewSet(viewsets.ModelViewSet):
    """Infrastructure inspection management"""
    queryset = InfrastructureInspection.objects.all()
    serializer_class = InfrastructureInspectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(inspector=self.request.user)
