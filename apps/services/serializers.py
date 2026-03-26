# apps/services/serializers.py
from rest_framework import serializers
from .models import Service


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'duration_minutes', 'price',
            'category', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'duration_minutes',
            'price', 'category', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'duration_minutes',
            'price', 'category'
        ]


class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'duration_minutes',
            'price', 'category', 'is_active'
        ]
