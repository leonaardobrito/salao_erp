# apps/accounts/repositories.py
from typing import Optional, List, Dict, Any
from django.db.models import QuerySet, Q
from django.core.paginator import Paginator
from .models import User


class UserRepository:
    """
    Repository for User data access.
    Implementa o padrão Repository para separar lógica de acesso a dados.
    """
    
    def __init__(self):
        self.model = User
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        try:
            return self.model.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        try:
            return self.model.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username"""
        try:
            return self.model.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            return None
    
    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Dict[str, Any] = None,
        search: str = None,
        order_by: str = '-date_joined'
    ) -> Dict[str, Any]:
        """
        Lista todos os usuários com paginação e filtros.
        """
        queryset = self.model.objects.filter(is_active=True)
        
        # Aplicar filtros
        if filters:
            queryset = queryset.filter(**filters)
        
        # Aplicar busca
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )
        
        # Ordenação
        queryset = queryset.order_by(order_by)
        
        # Paginação
        paginator = Paginator(queryset, page_size)
        users = paginator.get_page(page)
        
        return {
            'items': list(users),
            'total': paginator.count,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'has_next': users.has_next(),
            'has_previous': users.has_previous()
        }
    
    def get_by_role(self, role: str) -> List[User]:
        """Busca usuários por função"""
        return list(self.model.objects.filter(role=role, is_active=True))
    
    def get_professionals(self) -> List[User]:
        """Busca apenas profissionais"""
        return self.get_by_role('professional')
    
    def create(self, **data) -> User:
      """Cria um novo usuário"""
      # Extrair senha dos dados
      password = data.pop('password', None)
      
      # 🔥 Remover qualquer campo que não seja do modelo
      forbidden_fields = ['password2', 'profile']
      for field in forbidden_fields:
          if field in data:
              data.pop(field)
      
      # Criar usuário sem salvar ainda
      user = self.model(**data)
      
      # Definir senha
      if password:
          user.set_password(password)
      
      # Salvar usuário
      user.save()
      
      return user
      
    def update(self, user_id: int, **data) -> Optional[User]:
        """Atualiza um usuário existente"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in data.items():
            if key == 'password':
                user.set_password(value)
            else:
                setattr(user, key, value)
        
        user.save()
        return user
    
    def delete(self, user_id: int, hard: bool = False) -> bool:
        """Remove (soft ou hard delete) um usuário"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        if hard:
            user.delete()
        else:
            user.is_active = False
            user.save()
        
        return True
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """Conta usuários com filtros opcionais"""
        queryset = self.model.objects.filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        return queryset.count()
    
    def exists(self, **filters) -> bool:
        """Verifica se existe usuário com os filtros dados"""
        return self.model.objects.filter(**filters).exists()