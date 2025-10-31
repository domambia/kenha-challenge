"""
Blockchain serializers
"""
from rest_framework import serializers
from .models import BlockchainTransaction


class BlockchainTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainTransaction
        fields = ['id', 'transaction_type', 'entity_type', 'entity_id',
                 'transaction_hash', 'block_number', 'status',
                 'created_at', 'confirmed_at']
        read_only_fields = ['id', 'created_at']
