# apps/financial/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.dateparse import parse_date

from .models import Transaction
from .serializers import (
    TransactionListSerializer,
    TransactionDetailSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
)
from .services import TransactionService
from infrastructure.permissions import IsAdmin


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.filter(is_active=True).select_related(
        'appointment__customer', 'appointment__service'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'payment_method']
    search_fields = ['description', 'notes']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TransactionUpdateSerializer
        elif self.action == 'retrieve':
            return TransactionDetailSerializer
        return TransactionListSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            parsed = parse_date(date_from)
            if parsed:
                qs = qs.filter(transaction_date__gte=parsed)
        if date_to:
            parsed = parse_date(date_to)
            if parsed:
                qs = qs.filter(transaction_date__lte=parsed)
        return qs

    def perform_create(self, serializer):
        service = TransactionService()
        return service.create_transaction(serializer.validated_data)

    def perform_update(self, serializer):
        service = TransactionService()
        return service.update_transaction(
            self.get_object().id, serializer.validated_data
        )

    def perform_destroy(self, instance):
        service = TransactionService()
        service.delete_transaction(instance.id, hard=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        output_serializer = TransactionDetailSerializer(obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(TransactionDetailSerializer(instance).data)
