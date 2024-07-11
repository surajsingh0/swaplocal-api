from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'image', 'owner', 'owner_username', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'owner_username', 'created_at', 'updated_at']
