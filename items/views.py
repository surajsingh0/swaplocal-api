from rest_framework import viewsets, permissions
from .models import Item
from .serializers import ItemSerializer
from .utils import calculate_distance

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Item.objects.none()
        
        # Check if the user wants their own items
        get_own_items = self.request.query_params.get('own_items', 'false').lower() == 'true'

        if get_own_items:
            return Item.objects.filter(owner=user)
        
        if user.latitude is None or user.longitude is None:
            return Item.objects.none()

        # Get all items except the user's own
        all_items = Item.objects.exclude(owner=user)

        # Filter items based on distance
        nearby_items = [
            item for item in all_items
            if calculate_distance(user.latitude, user.longitude, item.owner.latitude, item.owner.longitude) <= user.max_distance
        ]

        return nearby_items

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)