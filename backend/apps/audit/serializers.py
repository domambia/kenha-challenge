"""
Audit log serializers
"""
from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True, allow_null=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user_email', 'action_type', 'entity_type', 'entity_id',
                 'action_details', 'ip_address', 'timestamp', 'blockchain_hash']
        read_only_fields = ['id', 'timestamp']
