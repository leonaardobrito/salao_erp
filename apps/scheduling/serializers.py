# apps/scheduling/serializers.py
from rest_framework import serializers
from .models import Appointment


class AppointmentListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    professional_name = serializers.CharField(
        source='professional.user.full_name', read_only=True
    )
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_name', 'professional', 'professional_name',
            'service', 'service_name', 'scheduled_at', 'status',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AppointmentDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    professional_name = serializers.CharField(
        source='professional.user.full_name', read_only=True
    )
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_name', 'professional', 'professional_name',
            'service', 'service_name', 'scheduled_at', 'status', 'notes',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'customer', 'professional', 'service',
            'scheduled_at', 'status', 'notes'
        ]


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['scheduled_at', 'status', 'notes', 'is_active']
