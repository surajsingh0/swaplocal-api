from django.db.models.signals import post_save
from django.dispatch import receiver
from exchanges.models import Exchange
from .models import Notification
from .tasks import send_notification

@receiver(post_save, sender=Exchange)
def create_exchange_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.receiver,
            level='info',
            actor=instance.initiator,
            verb='requested an exchange',
            target=instance,
            description=f"{instance.initiator.username} has requested to exchange {instance.item_offered.title} for your {instance.item_requested.title}."
        )
    elif instance.status == 'accepted':
        Notification.objects.create(
            user=instance.initiator,
            level='success',
            actor=instance.receiver,
            verb='accepted your exchange request',
            target=instance,
            description=f"{instance.receiver.username} has accepted your exchange request for {instance.item_requested.title}."
        )
    elif instance.status == 'rejected':
        Notification.objects.create(
            user=instance.initiator,
            level='warning',
            actor=instance.receiver,
            verb='rejected your exchange request',
            target=instance,
            description=f"{instance.receiver.username} has rejected your exchange request for {instance.item_requested.title}."
        )
    elif instance.status == 'completed':
        for user in [instance.initiator, instance.receiver]:
            Notification.objects.create(
                user=user,
                level='success',
                actor=instance,
                verb='has been completed',
                description=f"The exchange of {instance.item_offered.title} for {instance.item_requested.title} has been completed."
            )
        
    send_notification.delay(notification.id)