# apps/scheduling/admin.py
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'professional', 'service', 'scheduled_at', 'status']
    list_filter = ['status']
    search_fields = ['customer__name', 'professional__user__first_name']
