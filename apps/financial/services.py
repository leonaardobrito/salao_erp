# apps/financial/services.py
from typing import Dict, Any
from datetime import date
from django.db import transaction

from .models import Transaction
from .repositories import TransactionRepository
from infrastructure.exceptions import EntityNotFoundException


class TransactionService:
    def __init__(self):
        self.repository = TransactionRepository()

    def get_transaction(self, transaction_id: int) -> Transaction:
        txn = self.repository.get_by_id(transaction_id)
        if not txn:
            raise EntityNotFoundException('Transação não encontrada')
        return txn

    def list_transactions(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = '-transaction_date',
        date_from: date = None,
        date_to: date = None
    ) -> Dict[str, Any]:
        return self.repository.get_all(
            page=page, page_size=page_size,
            filters=filters, search=search, order_by=order_by,
            date_from=date_from, date_to=date_to
        )

    @transaction.atomic
    def create_transaction(self, data: Dict[str, Any]) -> Transaction:
        return self.repository.create(**data)

    @transaction.atomic
    def update_transaction(
        self, transaction_id: int, data: Dict[str, Any]
    ) -> Transaction:
        txn = self.repository.update(transaction_id, **data)
        if not txn:
            raise EntityNotFoundException('Transação não encontrada')
        return txn

    @transaction.atomic
    def delete_transaction(self, transaction_id: int, hard: bool = False) -> bool:
        return self.repository.delete(transaction_id, hard)
