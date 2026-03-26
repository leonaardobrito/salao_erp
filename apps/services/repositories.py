# apps/services/repositories.py
from typing import Optional, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Service


class ServiceRepository:
    def __init__(self):
        self.model = Service

    def get_by_id(self, service_id: int) -> Optional[Service]:
        try:
            return self.model.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
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

    def create(self, **data) -> Service:
        return self.model.objects.create(**data)

    def update(self, service_id: int, **data) -> Optional[Service]:
        service = self.get_by_id(service_id)
        if not service:
            return None
        for key, value in data.items():
            setattr(service, key, value)
        service.save()
        return service

    def delete(self, service_id: int, hard: bool = False) -> bool:
        service = self.get_by_id(service_id)
        if not service:
            return False
        if hard:
            service.delete()
        else:
            service.is_active = False
            service.save()
        return True
