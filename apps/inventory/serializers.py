# apps/inventory/serializers.py
from rest_framework import serializers
from .models import Stock, InventoryMovement


class StockListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'quantity', 'min_quantity', 'is_low_stock',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StockDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'quantity', 'min_quantity', 'is_low_stock',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['product', 'quantity', 'min_quantity']

    def validate_product(self, value):
        if Stock.objects.filter(product=value).exists():
            raise serializers.ValidationError(
                'Este produto já possui registro de estoque.'
            )
        return value


class StockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['quantity', 'min_quantity', 'is_active']


class MovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = InventoryMovement
        fields = [
            'id', 'product', 'product_name', 'quantity',
            'movement_type', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MovementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ['product', 'quantity', 'movement_type', 'notes']

    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError(
                'A quantidade não pode ser zero.'
            )
        return value
