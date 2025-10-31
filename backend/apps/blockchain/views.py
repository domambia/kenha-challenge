"""
Blockchain views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import BlockchainTransaction
from .serializers import BlockchainTransactionSerializer
from apps.incidents.models import Incident


class BlockchainTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """Blockchain transaction queries"""
    queryset = BlockchainTransaction.objects.all()
    serializer_class = BlockchainTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        entity_type = self.request.query_params.get('entity_type', None)
        entity_id = self.request.query_params.get('entity_id', None)
        if entity_type and entity_id:
            queryset = queryset.filter(entity_type=entity_type, entity_id=entity_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def notarize_incident(self, request):
        """Trigger blockchain notarization for an incident"""
        incident_id = request.data.get('incident_id')
        incident = get_object_or_404(Incident, incident_id=incident_id)
        
        # TODO: Implement actual blockchain notarization logic
        # This would interact with Base network via web3.py
        
        return Response({
            'message': 'Incident notarization initiated',
            'incident_id': incident_id
        }, status=status.HTTP_200_OK)
