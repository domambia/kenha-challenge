from django.contrib import admin
from .models import AIVerificationResult, HumanReview


@admin.register(AIVerificationResult)
class AIVerificationResultAdmin(admin.ModelAdmin):
    list_display = ['incident', 'model_version', 'classification_result', 'confidence_score', 'created_at']
    list_filter = ['classification_result', 'model_version', 'created_at']
    search_fields = ['incident__incident_id']


@admin.register(HumanReview)
class HumanReviewAdmin(admin.ModelAdmin):
    list_display = ['incident', 'reviewer', 'review_type', 'review_status', 'reviewed_at']
    list_filter = ['review_type', 'review_status', 'reviewed_at']
    search_fields = ['incident__incident_id', 'reviewer__email']

