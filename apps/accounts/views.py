from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import authenticate

from accounts.models import User
from accounts.serializers import (
    UserListSerializer, UserDetailSerializer, UserCreateSerializer,
    UserUpdateSerializer, ChangePasswordSerializer, LoginSerializer
)
from accounts.services import UserService
from infrastructure.permissions import IsAdmin, IsOwnerOrAdmin
from infrastructure.exceptions import BusinessRuleViolation, EntityNotFoundException


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada para login com JWT
    """
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Gerar tokens manualmente
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de usuários.
    """
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'username', 'phone']
    ordering_fields = ['first_name', 'last_name', 'date_joined', 'last_login']
    ordering = ['first_name']
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserListSerializer
    
    def get_permissions(self):
        """Define permissões especiais para algumas ações"""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'toggle_status']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filtra queryset baseado no usuário"""
        user = self.request.user
        
        # Se não estiver autenticado (criação de usuário), retorna vazio
        if not user.is_authenticated:
            return self.queryset.none()
        
        # Admin vê todos
        if user.is_admin:
            return self.queryset
        
        # Usuário comum vê apenas a si mesmo
        return self.queryset.filter(id=user.id)
    
    def get_object(self):
        """Retorna o objeto com verificação de permissão"""
        obj = super().get_object()
        
        # Verificar se usuário pode acessar este objeto
        if not self.request.user.is_admin and obj.id != self.request.user.id:
            self.permission_denied(
                self.request,
                message='Você não tem permissão para acessar este usuário.'
            )
        
        return obj
    
    def perform_create(self, serializer):
        """Cria um novo usuário"""
        service = UserService()
        service.create_user(serializer.validated_data)
    
    def perform_update(self, serializer):
        """Atualiza um usuário"""
        service = UserService()
        service.update_user(self.get_object().id, serializer.validated_data)
    
    def perform_destroy(self, instance):
        """Remove um usuário (soft delete)"""
        service = UserService()
        service.delete_user(instance.id, hard=False)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna os dados do usuário logado"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Altera a senha do usuário"""
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            service = UserService()
            service.change_password(
                user.id,
                serializer.validated_data['old_password'],
                serializer.validated_data['new_password']
            )
            return Response(
                {'detail': 'Senha alterada com sucesso.'},
                status=status.HTTP_200_OK
            )
        except (EntityNotFoundException, BusinessRuleViolation) as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def professionals(self, request):
        """Lista todos os profissionais"""
        service = UserService()
        professionals = service.get_professionals()
        serializer = self.get_serializer(professionals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Ativa/desativa um usuário"""
        user = self.get_object()
        
        try:
            service = UserService()
            user = service.toggle_user_status(user.id)
            status_text = 'ativado' if user.is_active else 'desativado'
            return Response({
                'detail': f'Usuário {status_text} com sucesso.',
                'is_active': user.is_active
            })
        except BusinessRuleViolation as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
