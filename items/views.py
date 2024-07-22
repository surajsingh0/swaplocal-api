from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Item
from exchanges.models import Exchange
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
        
        # Get items that have been part of completed exchanges
        completed_exchanges = Exchange.objects.filter(status='completed').values_list('item_offered_id', 'item_requested_id')
        completed_item_ids = set([item for sublist in completed_exchanges for item in sublist])
        
        # Check if the user wants their own items
        get_own_items = self.request.query_params.get('own_items', 'false').lower() == 'true'

        if get_own_items:
            items = Item.objects.filter(owner=user).exclude(id__in=completed_item_ids).select_related('owner')
            for item in items:
                exchange = Exchange.objects.filter(
                    Q(item_offered=item) | Q(item_requested=item),
                    status__in=['pending', 'accepted']
                ).first()
                item.exchange_status = exchange.status if exchange else None
            return items
        
        if user.latitude is None or user.longitude is None:
            return Item.objects.none()

        # Exclude items that are part of active exchanges
        active_exchanges = Exchange.objects.filter(
            status__in=['pending', 'accepted']
        ).values_list('item_offered_id', 'item_requested_id')
        excluded_item_ids = set([item for sublist in active_exchanges for item in sublist])
        excluded_item_ids.update(completed_item_ids)
        
        # Get all items except the user's own
        all_items = Item.objects.exclude(
            owner=user
        ).exclude(
            id__in=excluded_item_ids
        ).select_related('owner')
        
        # Calculate distances and filter
        items_with_distance = []
        for item in all_items:
            distance = calculate_distance(user.latitude, user.longitude, item.owner.latitude, item.owner.longitude)
            max_distance = max(user.max_distance, item.owner.max_distance)
            if distance <= max_distance:
                item.distance = distance  # Add distance as an attribute to the item
                items_with_distance.append(item)

        # Sort items by distance
        return sorted(items_with_distance, key=lambda x: x.distance)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)