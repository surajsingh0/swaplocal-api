from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Item
from exchanges.models import Exchange
from .serializers import ItemSerializer
from .utils import calculate_distance
from django.shortcuts import get_object_or_404

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

    # Future optimizations for pagination and own items
    # def _get_own_items(self, user):
    #     items = Item.objects.filter(owner=user).exclude(
    #         id__in=self._get_completed_item_ids()
    #     ).select_related('owner').annotate(
    #         exchange_status=Subquery(
    #             Exchange.objects.filter(
    #                 Q(item_offered=OuterRef('pk')) | Q(item_requested=OuterRef('pk')),
    #                 status__in=['pending', 'accepted']
    #             ).values('status')[:1]
    #         )
    #     )
    #     return items

    # def _get_other_items(self, user):
    #     if user.latitude is None or user.longitude is None:
    #         return Item.objects.none()

    #     excluded_item_ids = self._get_excluded_item_ids()

    #     return Item.objects.exclude(
    #         owner=user
    #     ).exclude(
    #         id__in=excluded_item_ids
    #     ).select_related('owner').annotate(
    #         distance=Sqrt(
    #             Power(F('owner__latitude') - user.latitude, 2) +
    #             Power(F('owner__longitude') - user.longitude, 2)
    #         )
    #     ).filter(
    #         distance__lte=F('owner__max_distance')
    #     ).order_by('distance')

    # def _get_completed_item_ids(self):
    #     return Exchange.objects.filter(
    #         status='completed'
    #     ).values_list('item_offered_id', 'item_requested_id')

    # def _get_excluded_item_ids(self):
    #     completed_item_ids = self._get_completed_item_ids()
    #     active_item_ids = Exchange.objects.filter(
    #         status__in=['pending', 'accepted']
    #     ).values_list('item_offered_id', 'item_requested_id')
    #     return set([item for sublist in completed_item_ids for item in sublist] +
    #                [item for sublist in active_item_ids for item in sublist])

    def get_object(self):
        return get_object_or_404(Item, pk=self.kwargs.get('pk'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

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