"""
Incident serializers
"""
from rest_framework import serializers
from .models import Incident, IncidentType, IncidentSeverity, IncidentComment


class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentType
        fields = ['id', 'name', 'category', 'description', 'icon']


class IncidentSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentSeverity
        fields = ['level', 'name', 'description', 'response_time_target_minutes', 'color_code']


class IncidentSerializer(serializers.ModelSerializer):
    incident_type = IncidentTypeSerializer(read_only=True)
    incident_type_id = serializers.IntegerField(write_only=True, required=False)
    # Accept 'incident_type' as integer ID for backward compatibility
    severity = IncidentSeveritySerializer(read_only=True)
    severity_level = serializers.CharField(write_only=True, required=False, max_length=10)
    # Accept 'severity' as string level for backward compatibility
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'incident_id', 'incident_type', 'incident_type_id', 'severity', 'severity_level', 'status', 'description',
            'latitude', 'longitude', 'road_name', 'timestamp', 'weather',
            'verification_status', 'ai_confidence_score', 'created_at', 'updated_at',
            'reporter_email', 'is_anonymous'
        ]
        read_only_fields = ['incident_id', 'created_at', 'updated_at']
    
    def to_internal_value(self, data):
        # Handle backward compatibility: map field names
        if isinstance(data, dict):
            needs_copy = False
            # Check if we need to map 'incident_type' to 'incident_type_id'
            if 'incident_type' in data and 'incident_type_id' not in data:
                needs_copy = True
            # Check if we need to map 'severity' to 'severity_level'
            if 'severity' in data and 'severity_level' not in data:
                needs_copy = True
            
            if needs_copy:
                # Create a copy to avoid mutating the original
                data = dict(data)
                if 'incident_type' in data and 'incident_type_id' not in data:
                    data['incident_type_id'] = data['incident_type']
                if 'severity' in data and 'severity_level' not in data:
                    data['severity_level'] = data['severity']
        
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        # Extract write-only fields
        incident_type_id = validated_data.pop('incident_type_id', None)
        severity_level = validated_data.pop('severity_level', None)
        
        # Get the IncidentType object
        if incident_type_id:
            try:
                incident_type = IncidentType.objects.get(id=incident_type_id)
                validated_data['incident_type'] = incident_type
            except IncidentType.DoesNotExist:
                raise serializers.ValidationError({
                    'incident_type': f'Incident type with id "{incident_type_id}" does not exist'
                })
        else:
            raise serializers.ValidationError({
                'incident_type': 'This field is required.'
            })
        
        # Get the IncidentSeverity object by level (e.g., "P1")
        if severity_level:
            try:
                severity = IncidentSeverity.objects.get(level=severity_level)
                validated_data['severity'] = severity
            except IncidentSeverity.DoesNotExist:
                raise serializers.ValidationError({
                    'severity': f'Severity level "{severity_level}" does not exist'
                })
        else:
            raise serializers.ValidationError({
                'severity': 'This field is required.'
            })
        
        return super().create(validated_data)


class IncidentCommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = IncidentComment
        fields = ['id', 'user_email', 'comment_text', 'comment_type', 'created_at']
        read_only_fields = ['id', 'created_at']

