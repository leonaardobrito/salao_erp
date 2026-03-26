# apps/financial/serializers.py
from rest_framework import serializers
from .models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    appointment_info = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'description',
            'payment_method', 'transaction_date', 'appointment',
            'appointment_info', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_appointment_info(self, obj):
        if obj.appointment:
            return {
                'id': obj.appointment.id,
                'customer': obj.appointment.customer.name,
                'service': obj.appointment.service.name,
            }
        return None


class TransactionDetailSerializer(serializers.ModelSerializer):
    appointment_info = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'description',
            'payment_method', 'transaction_date', 'appointment',
            'appointment_info', 'notes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_appointment_info(self, obj):
        if obj.appointment:
            return {
                'id': obj.appointment.id,
                'customer': obj.appointment.customer.name,
                'service': obj.appointment.service.name,
                'scheduled_at': obj.appointment.scheduled_at,
            }
        return None


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_type', 'amount', 'description',
            'payment_method', 'transaction_date', 'appointment', 'notes'
        ]


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_type', 'amount', 'description',
            'payment_method', 'transaction_date', 'appointment',
            'notes', 'is_active'
        ]
