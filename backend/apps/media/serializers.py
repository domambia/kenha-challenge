from rest_framework import serializers
from .models import MediaAsset
import hashlib
import os
import uuid
from django.core.files.storage import default_storage


class MediaAssetSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    incident_id = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = MediaAsset
        fields = ['id', 'asset_type', 'file', 'incident_id', 'file_path', 'file_hash', 'thumbnail_path', 
                 'created_at', 'faces_redacted', 'license_plates_redacted', 'file_size', 'mime_type', 'original_filename']
        read_only_fields = ['id', 'created_at', 'file_path', 'file_hash', 'file_size', 'mime_type', 'original_filename']
    
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        incident_id = validated_data.pop('incident_id', None)
        
        if not file:
            raise serializers.ValidationError({'file': 'File is required.'})
        
        # Calculate file hash
        file.seek(0)
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)
        
        # Determine asset type from file
        mime_type = file.content_type
        if mime_type.startswith('image/'):
            asset_type = 'photo'
        elif mime_type.startswith('video/'):
            asset_type = 'video'
        elif mime_type.startswith('audio/'):
            asset_type = 'audio'
        else:
            asset_type = validated_data.get('asset_type', 'photo')
        
        # Save file
        # Generate unique filename to avoid collisions
        file_extension = os.path.splitext(file.name)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = default_storage.save(
            f'incidents/{incident_id or "temp"}/{unique_filename}',
            file
        )
        
        # Build full URL - use request if available, otherwise construct from settings
        try:
            request = self.context.get('request')
            if request:
                # Get relative URL from storage
                relative_url = default_storage.url(file_path)
                # Build absolute URL
                file_url = request.build_absolute_uri(relative_url)
            else:
                file_url = default_storage.url(file_path)
        except Exception as e:
            # Fallback if request context not available
            file_url = default_storage.url(file_path)
        
        # Create MediaAsset
        validated_data.update({
            'asset_type': asset_type,
            'file_path': file_url,
            'file_hash': file_hash,
            'file_size': file.size,
            'mime_type': mime_type,
            'original_filename': file.name,
        })
        
        media_asset = MediaAsset(**validated_data)
        media_asset.save()
        
        return media_asset

