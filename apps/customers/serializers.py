# apps/customers/serializers.py
from rest_framework import serializers
from .models import Customer


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'document',
            'address', 'address_number', 'neighborhood', 'city', 'state', 'zip_code',
            'notes', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name', 'email', 'phone', 'document',
            'address', 'address_number', 'neighborhood', 'city', 'state', 'zip_code',
            'notes'
        ]


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name', 'email', 'phone', 'document',
            'address', 'address_number', 'neighborhood', 'city', 'state', 'zip_code',
            'notes', 'is_active'
        ]
