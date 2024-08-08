from django.db import models
from users.models import User
from items.models import Item

class Exchange(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_exchanges')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_exchanges')
    item_offered = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='offered_in_exchanges')
    item_requested = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requested_in_exchanges')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Send notification when an exchange is created, accepted, rejected, or completed
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification

@receiver(post_save, sender=Exchange)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Notify the receiver that an exchange has been initiated
        message = f"{instance.initiator.username} has initiated an exchange for your item '{instance.item_requested.title}'."
        Notification.objects.create(user=instance.receiver, exchange=instance, message=message)
    else:
        # Notify both initiator and receiver based on the status change
        if instance.status == 'accepted':
            message = f"Your exchange request for '{instance.item_requested.title}' has been accepted."
            Notification.objects.create(user=instance.initiator, exchange=instance, message=message)
        elif instance.status == 'rejected':
            message = f"Your exchange request for '{instance.item_requested.title}' has been rejected."
            Notification.objects.create(user=instance.initiator, exchange=instance, message=message)
        elif instance.status == 'completed':
            message = f"The exchange for '{instance.item_requested.title}' has been completed."
            Notification.objects.create(user=instance.initiator, exchange=instance, message=message)
            Notification.objects.create(user=instance.receiver, exchange=instance, message=message)
