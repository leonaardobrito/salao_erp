# apps/customers/repositories.py
from typing import Optional, List, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Customer


class CustomerRepository:
    def __init__(self):
        self.model = Customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
            return self.model.objects.get(id=customer_id, is_active=True)
        except Customer.DoesNotExist:
            return None

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'name'
    ) -> Dict[str, Any]:
        queryset = self.model.objects.filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(document__icontains=search)
            )
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

    def create(self, **data) -> Customer:
        return self.model.objects.create(**data)

    def update(self, customer_id: int, **data) -> Optional[Customer]:
        customer = self.get_by_id(customer_id)
        if not customer:
            return None
        for key, value in data.items():
            setattr(customer, key, value)
        customer.save()
        return customer

    def delete(self, customer_id: int, hard: bool = False) -> bool:
        customer = self.get_by_id(customer_id)
        if not customer:
            return False
        if hard:
            customer.delete()
        else:
            customer.is_active = False
            customer.save()
        return True
