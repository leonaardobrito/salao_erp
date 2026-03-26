# apps/services/services.py
from typing import Dict, Any
from django.db import transaction

from .models import Service
from .repositories import ServiceRepository
from infrastructure.exceptions import EntityNotFoundException


class ServiceService:
    def __init__(self):
        self.repository = ServiceRepository()

    def get_service(self, service_id: int) -> Service:
        service = self.repository.get_by_id(service_id)
        if not service:
            raise EntityNotFoundException('Serviço não encontrado')
        return service

    def list_services(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'name'
    ) -> Dict[str, Any]:
        return self.repository.get_all(
            page=page, page_size=page_size,
            filters=filters, search=search, order_by=order_by
        )

    @transaction.atomic
    def create_service(self, data: Dict[str, Any]) -> Service:
        return self.repository.create(**data)

    @transaction.atomic
    def update_service(self, service_id: int, data: Dict[str, Any]) -> Service:
        service = self.repository.update(service_id, **data)
        if not service:
            raise EntityNotFoundException('Serviço não encontrado')
        return service

    @transaction.atomic
    def delete_service(self, service_id: int, hard: bool = False) -> bool:
        return self.repository.delete(service_id, hard)
