# apps/inventory/views.py
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Stock, InventoryMovement
from .serializers import (
    StockListSerializer,
    StockDetailSerializer,
    StockCreateSerializer,
    StockUpdateSerializer,
    MovementSerializer,
    MovementCreateSerializer,
)
from .services import StockService
from infrastructure.permissions import IsAdmin
from infrastructure.exceptions import (
    EntityNotFoundException,
    BusinessRuleViolation,
    DuplicateEntityException
)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.filter(is_active=True).select_related('product')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['product__name', 'product__sku']
    ordering_fields = ['quantity', 'product__name', 'created_at']
    ordering = ['product__name']

    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StockUpdateSerializer
        elif self.action == 'retrieve':
            return StockDetailSerializer
        return StockListSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('low_stock') == 'true':
            qs = qs.filter(min_quantity__gt=0).filter(
                quantity__lte=models.F('min_quantity')
            )
        return qs

    def perform_create(self, serializer):
        service = StockService()
        return service.create_stock(serializer.validated_data)

    def perform_update(self, serializer):
        service = StockService()
        return service.update_stock(self.get_object().id, serializer.validated_data)

    def perform_destroy(self, instance):
        service = StockService()
        service.delete_stock(instance.id, hard=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        output_serializer = StockDetailSerializer(obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(StockDetailSerializer(instance).data)

    @action(detail=False, methods=['post'])
    def movement(self, request):
        """Registra uma movimentação de estoque"""
        serializer = MovementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = StockService()
            movement = service.add_movement(
                product_id=data['product'].id,
                quantity=data['quantity'],
                movement_type=data['movement_type'],
                notes=data.get('notes', '')
            )
            return Response(
                MovementSerializer(movement).data,
                status=status.HTTP_201_CREATED
            )
        except (EntityNotFoundException, BusinessRuleViolation) as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
