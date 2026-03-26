# apps/inventory/repositories.py
from typing import Optional, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Stock, InventoryMovement


class StockRepository:
    def __init__(self):
        self.model = Stock

    def get_by_id(self, stock_id: int) -> Optional[Stock]:
        try:
            return self.model.objects.select_related('product').get(
                id=stock_id, is_active=True
            )
        except Stock.DoesNotExist:
            return None

    def get_by_product(self, product_id: int) -> Optional[Stock]:
        try:
            return self.model.objects.select_related('product').get(
                product_id=product_id, is_active=True
            )
        except Stock.DoesNotExist:
            return None

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'product__name',
        low_stock_only: bool = False
    ) -> Dict[str, Any]:
        queryset = self.model.objects.select_related('product').filter(
            is_active=True
        )
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(product__name__icontains=search) |
                Q(product__sku__icontains=search)
            )
        if low_stock_only:
            queryset = queryset.filter(
                min_quantity__gt=0
            ).extra(
                where=['quantity <= min_quantity']
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

    def create(self, **data) -> Stock:
        return self.model.objects.create(**data)

    def update(self, stock_id: int, **data) -> Optional[Stock]:
        stock = self.get_by_id(stock_id)
        if not stock:
            return None
        for key, value in data.items():
            setattr(stock, key, value)
        stock.save()
        return stock

    def delete(self, stock_id: int, hard: bool = False) -> bool:
        stock = self.get_by_id(stock_id)
        if not stock:
            return False
        if hard:
            stock.delete()
        else:
            stock.is_active = False
            stock.save()
        return True


class MovementRepository:
    def __init__(self):
        self.model = InventoryMovement

    def create(self, **data) -> InventoryMovement:
        return self.model.objects.create(**data)
