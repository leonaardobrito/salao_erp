# apps/products/services.py
from typing import Dict, Any
from django.db import transaction

from .models import Product
from .repositories import ProductRepository
from infrastructure.exceptions import EntityNotFoundException


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise EntityNotFoundException('Produto não encontrado')
        return product

    def list_products(
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
    def create_product(self, data: Dict[str, Any]) -> Product:
        return self.repository.create(**data)

    @transaction.atomic
    def update_product(self, product_id: int, data: Dict[str, Any]) -> Product:
        product = self.repository.update(product_id, **data)
        if not product:
            raise EntityNotFoundException('Produto não encontrado')
        return product

    @transaction.atomic
    def delete_product(self, product_id: int, hard: bool = False) -> bool:
        return self.repository.delete(product_id, hard)
