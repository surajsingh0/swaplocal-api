from rest_framework import serializers
from .models import Item
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'max_distance']

class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'image', 'owner', 'created_at', 'updated_at', 'distance']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'distance']