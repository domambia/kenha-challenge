from django.contrib import admin
from .models import WorkOrder, InfrastructureInspection


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_type', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['work_type', 'status', 'priority', 'created_at']
    search_fields = ['description', 'completion_notes']


@admin.register(InfrastructureInspection)
class InfrastructureInspectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_order', 'inspector', 'inspection_date', 'repair_needed', 'priority']
    list_filter = ['inspection_type', 'repair_needed', 'priority', 'inspection_date']
    search_fields = ['inspection_report']

