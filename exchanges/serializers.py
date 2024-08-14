from rest_framework import serializers
from .models import Exchange
from items.serializers import ItemSerializer
from items.utils import calculate_distance

class ExchangeSerializer(serializers.ModelSerializer):
    initiator_username = serializers.ReadOnlyField(source='initiator.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    item_offered_title = serializers.ReadOnlyField(source='item_offered.title')
    item_requested_title = serializers.ReadOnlyField(source='item_requested.title')

    item_offered_item = serializers.SerializerMethodField()
    item_requested_item = serializers.SerializerMethodField()

    class Meta:
        model = Exchange
        fields = ['id', 'initiator', 'initiator_username', 'receiver', 'receiver_username', 
                  'item_offered', 'item_requested',
                  'item_offered_item', 'item_offered_title', 'item_requested_item', 'item_requested_title', 
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['initiator', 'initiator_username', 'receiver_username', 
                            'item_offered_title', 'item_requested_title', 'created_at', 'updated_at']
        
        
    def get_item_offered_item(self, obj):
        item = obj.item_offered
        user = self.context['request'].user
        if user.latitude is not None and user.longitude is not None:
            item.distance = calculate_distance(item.owner.latitude, item.owner.longitude, user.latitude, user.longitude)
        else:
            item.distance = None
        return ItemSerializer(item).data

    def get_item_requested_item(self, obj):
        item = obj.item_requested
        user = self.context['request'].user
        if user.latitude is not None and user.longitude is not None:
            item.distance = calculate_distance(item.owner.latitude, item.owner.longitude, user.latitude, user.longitude)
        else:
            item.distance = None
        return ItemSerializer(item).data