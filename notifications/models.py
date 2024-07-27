from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    LEVELS = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    level = models.CharField(max_length=20, choices=LEVELS, default='info')
    unread = models.BooleanField(default=True)
    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor', on_delete=models.CASCADE)
    actor_object_id = models.CharField(max_length=255)
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', on_delete=models.CASCADE, blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target or ''}"