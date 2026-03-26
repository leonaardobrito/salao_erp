# apps/scheduling/repositories.py
from typing import Optional, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, date

from .models import Appointment


class AppointmentRepository:
    def __init__(self):
        self.model = Appointment

    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        try:
            return self.model.objects.select_related(
                'customer', 'professional__user', 'service'
            ).get(id=appointment_id, is_active=True)
        except Appointment.DoesNotExist:
            return None

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = '-scheduled_at',
        date_from: date = None,
        date_to: date = None,
        professional_id: int = None
    ) -> Dict[str, Any]:
        queryset = self.model.objects.select_related(
            'customer', 'professional__user', 'service'
        ).filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(customer__name__icontains=search) |
                Q(professional__user__first_name__icontains=search) |
                Q(professional__user__last_name__icontains=search) |
                Q(service__name__icontains=search)
            )
        if date_from:
            queryset = queryset.filter(scheduled_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(scheduled_at__date__lte=date_to)
        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)
        queryset = queryset.order_by(order_by)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        return {
            'items': list(page_obj),
            'total': paginator.count,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
        }

    def create(self, **data) -> Appointment:
        return self.model.objects.create(**data)

    def update(self, appointment_id: int, **data) -> Optional[Appointment]:
        appointment = self.get_by_id(appointment_id)
        if not appointment:
            return None
        for key, value in data.items():
            setattr(appointment, key, value)
        appointment.save()
        return appointment

    def delete(self, appointment_id: int, hard: bool = False) -> bool:
        appointment = self.get_by_id(appointment_id)
        if not appointment:
            return False
        if hard:
            appointment.delete()
        else:
            appointment.is_active = False
            appointment.save()
        return True
