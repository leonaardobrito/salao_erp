# apps/accounts/services.py
from typing import Optional, Dict, Any, List
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .repositories import UserRepository
from .models import User, UserProfile
from infrastructure.exceptions import (
    BusinessRuleViolation,
    EntityNotFoundException,
    DuplicateEntityException
)


class UserService:
    """
    Service layer for User business logic.
    Implementa casos de uso e regras de negócio.
    """
    
    def __init__(self):
        self.repository = UserRepository()
    
    def get_user(self, user_id: int) -> User:
        """Busca um usuário pelo ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException('Usuário não encontrado')
        return user
    
    def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = '-date_joined'
    ) -> Dict[str, Any]:
        """Lista usuários com paginação"""
        return self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            search=search,
            order_by=order_by
        )
    
    @transaction.atomic
    def create_user(self, data: Dict[str, Any]) -> User:
        """Cria um novo usuário com validações"""
        # Validar email único
        email = data.get('email')
        if email and self.repository.exists(email=email):
            raise DuplicateEntityException('Email já cadastrado')
        
        # Validar username único
        username = data.get('username')
        if username and self.repository.exists(username=username):
            raise DuplicateEntityException('Nome de usuário já existe')
        
        # Validar documento único
        document = data.get('document')
        if document and self.repository.exists(document=document):
            raise DuplicateEntityException('Documento já cadastrado')
        
        # 🔥 IMPORTANTE: Remover password2 antes de criar
        if 'password2' in data:
            data.pop('password2')
        
        # Separar dados do perfil
        profile_data = data.pop('profile', {})
        
        # Criar usuário
        user = self.repository.create(**data)
        
        # Criar perfil se não existir
        if profile_data:
            UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        else:
            UserProfile.objects.get_or_create(user=user)
    
        return user

    @transaction.atomic
    def update_user(self, user_id: int, data: Dict[str, Any]) -> User:
        """Atualiza um usuário existente"""
        user = self.get_user(user_id)
        
        # Validar email único (se alterado)
        email = data.get('email')
        if email and email != user.email:
            if self.repository.exists(email=email):
                raise DuplicateEntityException('Email já cadastrado')
        
        # Validar documento único (se alterado)
        document = data.get('document')
        if document and document != user.document:
            if self.repository.exists(document=document):
                raise DuplicateEntityException('Documento já cadastrado')
        
        # Atualizar
        updated_user = self.repository.update(user_id, **data)
        if not updated_user:
            raise EntityNotFoundException('Usuário não encontrado')
        
        return updated_user
    
    @transaction.atomic
    def delete_user(self, user_id: int, hard: bool = False) -> bool:
        """Remove um usuário"""
        user = self.get_user(user_id)
        
        # Regra de negócio: não permitir deletar último admin
        if user.role == 'admin' and not hard:
            admin_count = self.repository.count({'role': 'admin'})
            if admin_count <= 1:
                raise BusinessRuleViolation(
                    'Não é possível remover o último administrador do sistema'
                )
        
        return self.repository.delete(user_id, hard)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Autentica um usuário"""
        user = authenticate(username=username, password=password)
        
        if not user:
            raise BusinessRuleViolation('Credenciais inválidas')
        
        if not user.is_active:
            raise BusinessRuleViolation('Usuário inativo')
        
        # Atualizar último acesso
        user.update_last_access()
        
        return user
    
    def generate_tokens(self, user: User) -> Dict[str, str]:
        """Gera tokens JWT para o usuário"""
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }
    
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """Altera a senha do usuário"""
        user = self.get_user(user_id)
        
        if not user.check_password(old_password):
            raise BusinessRuleViolation('Senha atual incorreta')
        
        user.set_password(new_password)
        user.save()
        
        return True
    
    def get_professionals(self) -> List[User]:
        """Retorna lista de profissionais"""
        return self.repository.get_professionals()
    
    def toggle_user_status(self, user_id: int) -> User:
        """Ativa/desativa um usuário"""
        user = self.get_user(user_id)
        
        # Não permitir desativar último admin
        if user.is_active and user.role == 'admin':
            admin_count = self.repository.count({'role': 'admin', 'is_active': True})
            if admin_count <= 1:
                raise BusinessRuleViolation(
                    'Não é possível desativar o último administrador do sistema'
                )
        
        user.is_active = not user.is_active
        user.save()
        
        return user