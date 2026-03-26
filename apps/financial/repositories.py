# apps/financial/repositories.py
from typing import Optional, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date

from .models import Transaction


class TransactionRepository:
    def __init__(self):
        self.model = Transaction

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        try:
            return self.model.objects.select_related('appointment').get(
                id=transaction_id, is_active=True
            )
        except Transaction.DoesNotExist:
            return None

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = '-transaction_date',
        date_from: date = None,
        date_to: date = None
    ) -> Dict[str, Any]:
        queryset = self.model.objects.select_related('appointment').filter(
            is_active=True
        )
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) | Q(notes__icontains=search)
            )
        if date_from:
            queryset = queryset.filter(transaction_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(transaction_date__lte=date_to)
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

    def create(self, **data) -> Transaction:
        return self.model.objects.create(**data)

    def update(self, transaction_id: int, **data) -> Optional[Transaction]:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None
        for key, value in data.items():
            setattr(transaction, key, value)
        transaction.save()
        return transaction

    def delete(self, transaction_id: int, hard: bool = False) -> bool:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return False
        if hard:
            transaction.delete()
        else:
            transaction.is_active = False
            transaction.save()
        return True
