# apps/professionals/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Professional
from .serializers import (
    ProfessionalListSerializer,
    ProfessionalDetailSerializer,
    ProfessionalCreateSerializer,
    ProfessionalUpdateSerializer,
)
from .services import ProfessionalService
from infrastructure.permissions import IsAdmin
from infrastructure.exceptions import EntityNotFoundException, DuplicateEntityException


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.filter(is_active=True).select_related('user')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email', 'specialties'
    ]
    ordering_fields = ['user__first_name', 'created_at']
    ordering = ['user__first_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfessionalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProfessionalUpdateSerializer
        elif self.action == 'retrieve':
            return ProfessionalDetailSerializer
        return ProfessionalListSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        service = ProfessionalService()
        return service.create_professional(serializer.validated_data)

    def perform_update(self, serializer):
        service = ProfessionalService()
        return service.update_professional(
            self.get_object().id, serializer.validated_data
        )

    def perform_destroy(self, instance):
        service = ProfessionalService()
        service.delete_professional(instance.id, hard=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        professional = self.perform_create(serializer)
        output_serializer = ProfessionalDetailSerializer(professional)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(ProfessionalDetailSerializer(instance).data)
