from rest_framework import serializers
from .models import MediaAsset


class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = ['id', 'asset_type', 'file_path', 'file_hash', 'thumbnail_path', 
                 'created_at', 'faces_redacted', 'license_plates_redacted']
        read_only_fields = ['id', 'created_at']

