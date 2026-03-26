# apps/professionals/admin.py
from django.contrib import admin
from .models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['user', 'commission_percent', 'specialties', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
