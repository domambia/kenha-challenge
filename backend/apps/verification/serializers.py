"""
Verification and AI serializers
"""
from rest_framework import serializers
from .models import AIVerificationResult, HumanReview


class AIVerificationResultSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    
    class Meta:
        model = AIVerificationResult
        fields = ['id', 'incident_id', 'model_version', 'model_name',
                 'classification_result', 'confidence_score',
                 'duplicate_detection_score', 'credibility_score',
                 'processing_time', 'model_metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class HumanReviewSerializer(serializers.ModelSerializer):
    incident_id = serializers.CharField(source='incident.incident_id', read_only=True)
    reviewer_email = serializers.EmailField(source='reviewer.email', read_only=True)
    
    class Meta:
        model = HumanReview
        fields = ['id', 'incident_id', 'reviewer_email', 'review_type',
                 'review_status', 'review_notes', 'review_duration_seconds',
                 'reviewed_at']
        read_only_fields = ['id', 'reviewed_at']
