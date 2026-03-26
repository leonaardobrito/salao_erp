# apps/customers/services.py
from typing import Dict, Any
from django.db import transaction

from .models import Customer
from .repositories import CustomerRepository
from infrastructure.exceptions import EntityNotFoundException


class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException('Cliente não encontrado')
        return customer

    def list_customers(
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
    def create_customer(self, data: Dict[str, Any]) -> Customer:
        return self.repository.create(**data)

    @transaction.atomic
    def update_customer(self, customer_id: int, data: Dict[str, Any]) -> Customer:
        customer = self.repository.update(customer_id, **data)
        if not customer:
            raise EntityNotFoundException('Cliente não encontrado')
        return customer

    @transaction.atomic
    def delete_customer(self, customer_id: int, hard: bool = False) -> bool:
        return self.repository.delete(customer_id, hard)
