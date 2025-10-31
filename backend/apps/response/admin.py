from django.contrib import admin
from .models import IncidentAssignment, ResponseMilestone, ResponderLocation, ResponderChecklist


@admin.register(IncidentAssignment)
class IncidentAssignmentAdmin(admin.ModelAdmin):
    list_display = ['incident', 'assigned_to', 'assignment_type', 'status', 'assigned_at']
    list_filter = ['status', 'assignment_type', 'assigned_at']
    search_fields = ['incident__incident_id', 'assigned_to__email']


@admin.register(ResponseMilestone)
class ResponseMilestoneAdmin(admin.ModelAdmin):
    list_display = ['incident', 'responder', 'milestone_type', 'timestamp']
    list_filter = ['milestone_type', 'timestamp']
    search_fields = ['incident__incident_id', 'responder__email']


@admin.register(ResponderLocation)
class ResponderLocationAdmin(admin.ModelAdmin):
    list_display = ['responder', 'latitude', 'longitude', 'timestamp', 'is_active']
    list_filter = ['is_active', 'timestamp']
    search_fields = ['responder__email']


@admin.register(ResponderChecklist)
class ResponderChecklistAdmin(admin.ModelAdmin):
    list_display = ['incident_type', 'responder_role', 'is_required', 'order']
    list_filter = ['responder_role', 'is_required']

