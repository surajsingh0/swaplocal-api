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
