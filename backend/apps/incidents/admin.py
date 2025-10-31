from django.contrib import admin
from .models import Incident, IncidentType, IncidentSeverity, IncidentComment, IncidentMessage


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'severity_template', 'default_sla_minutes', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']


@admin.register(IncidentSeverity)
class IncidentSeverityAdmin(admin.ModelAdmin):
    list_display = ['level', 'name', 'response_time_target_minutes', 'escalation_time_minutes', 'priority_score']
    ordering = ['priority_score']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'incident_type', 'severity', 'status', 'reporter', 'created_at', 'verification_status']
    list_filter = ['status', 'severity', 'verification_status', 'incident_type', 'created_at']
    search_fields = ['incident_id', 'description', 'road_name']
    readonly_fields = ['incident_id', 'incident_hash', 'blockchain_tx_hash', 'blockchain_timestamp']
    date_hierarchy = 'created_at'


@admin.register(IncidentComment)
class IncidentCommentAdmin(admin.ModelAdmin):
    list_display = ['incident', 'user', 'comment_type', 'created_at']
    list_filter = ['comment_type', 'created_at']
    search_fields = ['comment_text', 'user__email']


@admin.register(IncidentMessage)
class IncidentMessageAdmin(admin.ModelAdmin):
    list_display = ['incident', 'sender', 'recipient', 'message_type', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']

