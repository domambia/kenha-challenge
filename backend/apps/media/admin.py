from django.contrib import admin
from .models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident', 'asset_type', 'file_hash', 'virus_scan_status', 'created_at']
    list_filter = ['asset_type', 'virus_scan_status', 'created_at']
    search_fields = ['incident__incident_id', 'file_hash', 'original_filename']

