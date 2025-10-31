"""
Work order serializers
"""
from rest_framework import serializers
from .models import WorkOrder, InfrastructureInspection


class WorkOrderSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True, allow_null=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True, allow_null=True)
    
    class Meta:
        model = WorkOrder
        fields = ['id', 'incident_id', 'work_type', 'status', 'priority',
                 'description', 'latitude', 'longitude', 'assigned_to_email',
                 'estimated_duration', 'actual_duration', 'started_at',
                 'completed_at', 'completion_notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class InfrastructureInspectionSerializer(serializers.ModelSerializer):
    work_order_id = serializers.IntegerField(source='work_order.id', read_only=True)
    inspector_email = serializers.EmailField(source='inspector.email', read_only=True)
    
    class Meta:
        model = InfrastructureInspection
        fields = ['id', 'work_order_id', 'inspector_email', 'inspection_date',
                 'inspection_type', 'damage_assessment', 'repair_needed',
                 'priority', 'photos', 'inspection_report', 'created_at']
        read_only_fields = ['id', 'created_at']
