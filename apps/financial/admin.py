# apps/financial/admin.py
from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'description', 'transaction_type', 'amount',
        'payment_method', 'transaction_date', 'appointment'
    ]
    list_filter = ['transaction_type', 'payment_method']
    search_fields = ['description', 'notes']
