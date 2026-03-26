# apps/scheduling/services.py
from typing import Dict, Any, Optional
from datetime import date
from django.db import transaction

from .models import Appointment
from .repositories import AppointmentRepository
from infrastructure.exceptions import EntityNotFoundException


class AppointmentService:
    def __init__(self):
        self.repository = AppointmentRepository()

    def get_appointment(self, appointment_id: int) -> Appointment:
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            raise EntityNotFoundException('Agendamento não encontrado')
        return appointment

    def list_appointments(
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
        return self.repository.get_all(
            page=page, page_size=page_size,
            filters=filters, search=search, order_by=order_by,
            date_from=date_from, date_to=date_to,
            professional_id=professional_id
        )

    @transaction.atomic
    def create_appointment(self, data: Dict[str, Any]) -> Appointment:
        return self.repository.create(**data)

    @transaction.atomic
    def update_appointment(
        self, appointment_id: int, data: Dict[str, Any]
    ) -> Appointment:
        appointment = self.repository.update(appointment_id, **data)
        if not appointment:
            raise EntityNotFoundException('Agendamento não encontrado')
        return appointment

    @transaction.atomic
    def delete_appointment(self, appointment_id: int, hard: bool = False) -> bool:
        return self.repository.delete(appointment_id, hard)
