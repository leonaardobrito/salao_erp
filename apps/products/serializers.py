# apps/products/serializers.py
from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'unit_price', 'category',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'unit_price', 'cost_price',
            'category', 'unit', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'description', 'unit_price', 'cost_price',
            'category', 'unit'
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'description', 'unit_price', 'cost_price',
            'category', 'unit', 'is_active'
        ]
