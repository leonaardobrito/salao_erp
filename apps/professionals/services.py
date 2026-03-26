# apps/professionals/services.py
from typing import Dict, Any
from django.db import transaction

from .models import Professional
from .repositories import ProfessionalRepository
from infrastructure.exceptions import EntityNotFoundException, DuplicateEntityException


class ProfessionalService:
    def __init__(self):
        self.repository = ProfessionalRepository()

    def get_professional(self, professional_id: int) -> Professional:
        professional = self.repository.get_by_id(professional_id)
        if not professional:
            raise EntityNotFoundException('Profissional não encontrado')
        return professional

    def list_professionals(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = 'user__first_name'
    ) -> Dict[str, Any]:
        return self.repository.get_all(
            page=page, page_size=page_size,
            filters=filters, search=search, order_by=order_by
        )

    @transaction.atomic
    def create_professional(self, data: Dict[str, Any]) -> Professional:
        user_id = data.get('user')
        if hasattr(user_id, 'id'):
            user_id = user_id.id
        if self.repository.get_by_user(user_id):
            raise DuplicateEntityException(
                'Este usuário já possui um perfil profissional.'
            )
        return self.repository.create(**data)

    @transaction.atomic
    def update_professional(
        self, professional_id: int, data: Dict[str, Any]
    ) -> Professional:
        professional = self.repository.update(professional_id, **data)
        if not professional:
            raise EntityNotFoundException('Profissional não encontrado')
        return professional

    @transaction.atomic
    def delete_professional(self, professional_id: int, hard: bool = False) -> bool:
        return self.repository.delete(professional_id, hard)
