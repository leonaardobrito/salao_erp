# apps/inventory/admin.py
from django.contrib import admin
from .models import Stock, InventoryMovement


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'min_quantity', 'is_active']
    list_filter = ['is_active']
    search_fields = ['product__name', 'product__sku']


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'movement_type', 'created_at']
    list_filter = ['movement_type']
    search_fields = ['product__name']
