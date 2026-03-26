# apps/products/repositories.py
from typing import Optional, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Product


class ProductRepository:
    def __init__(self):
        self.model = Product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        try:
            return self.model.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
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
                Q(sku__icontains=search) |
                Q(description__icontains=search) |
                Q(category__icontains=search)
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

    def create(self, **data) -> Product:
        return self.model.objects.create(**data)

    def update(self, product_id: int, **data) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    def delete(self, product_id: int, hard: bool = False) -> bool:
        product = self.get_by_id(product_id)
        if not product:
            return False
        if hard:
            product.delete()
        else:
            product.is_active = False
            product.save()
        return True
