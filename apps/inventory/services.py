# apps/inventory/services.py
from typing import Dict, Any, Optional
from django.db import transaction

from .models import Stock, InventoryMovement
from .repositories import StockRepository, MovementRepository
from infrastructure.exceptions import (
    EntityNotFoundException,
    BusinessRuleViolation,
    DuplicateEntityException
)


class StockService:
    def __init__(self):
        self.stock_repo = StockRepository()
        self.movement_repo = MovementRepository()

    def get_stock(self, stock_id: int) -> Stock:
        stock = self.stock_repo.get_by_id(stock_id)
        if not stock:
            raise EntityNotFoundException('Estoque não encontrado')
        return stock

    def get_stock_by_product(self, product_id: int) -> Optional[Stock]:
        return self.stock_repo.get_by_product(product_id)

    def list_stocks(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'product__name',
        low_stock_only: bool = False
    ) -> Dict[str, Any]:
        return self.stock_repo.get_all(
            page=page, page_size=page_size,
            filters=filters, search=search, order_by=order_by,
            low_stock_only=low_stock_only
        )

    @transaction.atomic
    def create_stock(self, data: Dict[str, Any]) -> Stock:
        product = data.get('product')
        if hasattr(product, 'id'):
            product_id = product.id
        else:
            product_id = product
        if self.stock_repo.get_by_product(product_id):
            raise DuplicateEntityException(
                'Este produto já possui registro de estoque.'
            )
        return self.stock_repo.create(**data)

    @transaction.atomic
    def update_stock(self, stock_id: int, data: Dict[str, Any]) -> Stock:
        stock = self.stock_repo.update(stock_id, **data)
        if not stock:
            raise EntityNotFoundException('Estoque não encontrado')
        return stock

    @transaction.atomic
    def delete_stock(self, stock_id: int, hard: bool = False) -> bool:
        return self.stock_repo.delete(stock_id, hard)

    @transaction.atomic
    def add_movement(
        self,
        product_id: int,
        quantity: int,
        movement_type: str,
        notes: str = ''
    ) -> InventoryMovement:
        stock = self.stock_repo.get_by_product(product_id)
        if not stock:
            raise EntityNotFoundException(
                'Produto não possui registro de estoque.'
            )
        new_quantity = stock.quantity + quantity
        if new_quantity < 0:
            raise BusinessRuleViolation(
                f'Quantidade insuficiente em estoque. Disponível: {stock.quantity}'
            )
        movement = self.movement_repo.create(
            product_id=product_id,
            quantity=quantity,
            movement_type=movement_type,
            notes=notes
        )
        stock.quantity = new_quantity
        stock.save()
        return movement
