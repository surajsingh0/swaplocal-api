from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exchange
from .serializers import ExchangeSerializer

class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can see exchanges they're involved in
        return Exchange.objects.filter(initiator=self.request.user) | Exchange.objects.filter(receiver=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        exchange = self.get_object()
        if exchange.receiver != request.user:
            return Response({"detail": "You are not the receiver of this exchange."}, status=status.HTTP_403_FORBIDDEN)
        exchange.status = 'accepted'
        exchange.save()
        return Response({"detail": "Exchange accepted."})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        exchange = self.get_object()
        if exchange.receiver != request.user:
            return Response({"detail": "You are not the receiver of this exchange."}, status=status.HTTP_403_FORBIDDEN)
        exchange.status = 'rejected'
        exchange.save()
        return Response({"detail": "Exchange rejected."})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        exchange = self.get_object()
        if exchange.initiator != request.user and exchange.receiver != request.user:
            return Response({"detail": "You are not part of this exchange."}, status=status.HTTP_403_FORBIDDEN)
        if exchange.status != 'accepted':
            return Response({"detail": "This exchange is not in 'accepted' status."}, status=status.HTTP_400_BAD_REQUEST)
        exchange.status = 'completed'
        exchange.save()
        return Response({"detail": "Exchange completed."})

