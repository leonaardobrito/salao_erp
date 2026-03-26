# apps/scheduling/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.dateparse import parse_date

from .models import Appointment
from .serializers import (
    AppointmentListSerializer,
    AppointmentDetailSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer,
)
from .services import AppointmentService
from infrastructure.permissions import IsAdmin


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.filter(is_active=True).select_related(
        'customer', 'professional__user', 'service'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'professional', 'customer', 'service']
    search_fields = [
        'customer__name', 'professional__user__first_name',
        'professional__user__last_name', 'service__name'
    ]
    ordering_fields = ['scheduled_at', 'created_at']
    ordering = ['-scheduled_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentUpdateSerializer
        elif self.action == 'retrieve':
            return AppointmentDetailSerializer
        return AppointmentListSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        professional_id = self.request.query_params.get('professional')
        if date_from:
            parsed = parse_date(date_from)
            if parsed:
                qs = qs.filter(scheduled_at__date__gte=parsed)
        if date_to:
            parsed = parse_date(date_to)
            if parsed:
                qs = qs.filter(scheduled_at__date__lte=parsed)
        if professional_id:
            qs = qs.filter(professional_id=professional_id)
        return qs

    def perform_create(self, serializer):
        service = AppointmentService()
        return service.create_appointment(serializer.validated_data)

    def perform_update(self, serializer):
        service = AppointmentService()
        return service.update_appointment(
            self.get_object().id, serializer.validated_data
        )

    def perform_destroy(self, instance):
        service = AppointmentService()
        service.delete_appointment(instance.id, hard=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        output_serializer = AppointmentDetailSerializer(obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(AppointmentDetailSerializer(instance).data)
