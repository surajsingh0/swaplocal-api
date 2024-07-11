from rest_framework import serializers
from .models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    initiator_username = serializers.ReadOnlyField(source='initiator.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    item_offered_title = serializers.ReadOnlyField(source='item_offered.title')
    item_requested_title = serializers.ReadOnlyField(source='item_requested.title')

    class Meta:
        model = Exchange
        fields = ['id', 'initiator', 'initiator_username', 'receiver', 'receiver_username', 
                  'item_offered', 'item_offered_title', 'item_requested', 'item_requested_title', 
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['initiator', 'initiator_username', 'receiver_username', 
                            'item_offered_title', 'item_requested_title', 'created_at', 'updated_at']

