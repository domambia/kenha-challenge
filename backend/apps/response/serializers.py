"""
Response coordination serializers
"""
from rest_framework import serializers
from .models import IncidentAssignment, ResponseMilestone, ResponderLocation, ResponderChecklist


class IncidentAssignmentSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    assigned_by_email = serializers.EmailField(source='assigned_by.email', read_only=True)
    
    class Meta:
        model = IncidentAssignment
        fields = ['id', 'incident_id', 'assigned_to_email', 'assigned_by_email',
                 'assignment_type', 'status', 'assigned_at', 'accepted_at',
                 'completed_at', 'estimated_arrival_time', 'actual_arrival_time', 'notes']
        read_only_fields = ['id', 'assigned_at']


class ResponseMilestoneSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    responder_email = serializers.EmailField(source='responder.email', read_only=True)
    
    class Meta:
        model = ResponseMilestone
        fields = ['id', 'incident_id', 'responder_email', 'milestone_type',
                 'latitude', 'longitude', 'notes', 'media_attachments', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ResponderLocationSerializer(serializers.ModelSerializer):
    responder_email = serializers.EmailField(source='responder.email', read_only=True)
    
    class Meta:
        model = ResponderLocation
        fields = ['id', 'responder_email', 'latitude', 'longitude', 'timestamp',
                 'accuracy', 'speed', 'heading', 'is_active']
        read_only_fields = ['id', 'timestamp']


class ResponderChecklistSerializer(serializers.ModelSerializer):
    incident_type_name = serializers.CharField(source='incident_type.name', read_only=True)
    
    class Meta:
        model = ResponderChecklist
        fields = ['id', 'incident_type_name', 'responder_role', 'checklist_items',
                 'is_required', 'order']
        read_only_fields = ['id']
