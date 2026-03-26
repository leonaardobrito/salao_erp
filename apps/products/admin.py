# apps/products/admin.py
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'unit_price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'sku', 'category']
