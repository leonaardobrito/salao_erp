# apps/professionals/repositories.py
from typing import Optional, List, Dict, Any
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Professional


class ProfessionalRepository:
    def __init__(self):
        self.model = Professional

    def get_by_id(self, professional_id: int) -> Optional[Professional]:
        try:
            return self.model.objects.select_related('user').get(
                id=professional_id, is_active=True
            )
        except Professional.DoesNotExist:
            return None

    def get_by_user(self, user_id: int) -> Optional[Professional]:
        try:
            return self.model.objects.select_related('user').get(
                user_id=user_id, is_active=True
            )
        except Professional.DoesNotExist:
            return None

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'user__first_name'
    ) -> Dict[str, Any]:
        queryset = self.model.objects.select_related('user').filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(specialties__icontains=search)
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

    def create(self, **data) -> Professional:
        return self.model.objects.create(**data)

    def update(self, professional_id: int, **data) -> Optional[Professional]:
        professional = self.get_by_id(professional_id)
        if not professional:
            return None
        for key, value in data.items():
            setattr(professional, key, value)
        professional.save()
        return professional

    def delete(self, professional_id: int, hard: bool = False) -> bool:
        professional = self.get_by_id(professional_id)
        if not professional:
            return False
        if hard:
            professional.delete()
        else:
            professional.is_active = False
            professional.save()
        return True
