from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification

class ContentTypeField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.app_label}.{value.model}"

    def to_internal_value(self, data):
        app_label, model = data.split('.')
        return ContentType.objects.get(app_label=app_label, model=model)

class NotificationSerializer(serializers.ModelSerializer):
    actor_content_type = ContentTypeField(queryset=ContentType.objects.all())
    target_content_type = ContentTypeField(queryset=ContentType.objects.all(), allow_null=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'level', 'unread', 'actor_content_type', 'actor_object_id',
                  'verb', 'description', 'target_content_type', 'target_object_id',
                  'created_at']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['actor'] = str(instance.actor)
        if instance.target:
            representation['target'] = str(instance.target)
        return representation