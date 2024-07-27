from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from .serializers import NotificationSerializer

@shared_task
def send_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{notification.user.id}",
            {
                "type": "send_notification",
                "message": NotificationSerializer(notification).data
            }
        )
    except Notification.DoesNotExist:
        pass