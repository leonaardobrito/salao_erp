# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Modelo de usuário customizado.
    Estende o AbstractUser do Django adicionando campos específicos.
    """
    
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('receptionist', 'Recepcionista'),
        ('professional', 'Profissional'),
        ('customer', 'Cliente'),
    ]
    
    # Campos adicionais
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=20,
        validators=[phone_regex],
        blank=True,
        null=True
    )
    
    mobile = models.CharField(
        'Celular',
        max_length=20,
        validators=[phone_regex],
        blank=True,
        null=True
    )
    
    role = models.CharField(
        'Função',
        max_length=20,
        choices=ROLE_CHOICES,
        default='professional'
    )
    
    document = models.CharField(
        'CPF/CNPJ',
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    
    birth_date = models.DateField(
        'Data de Nascimento',
        null=True,
        blank=True
    )
    
    # Controle de acesso
    last_access = models.DateTimeField(
        'Último acesso',
        null=True,
        blank=True
    )
    
    # Auditoria
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name='Criado por'
    )
    
    # Metadados
    notes = models.TextField('Observações', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['document']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def save(self, *args, **kwargs):
        """Garantir que email seja único e em minúsculas"""
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Retorna o nome completo do usuário"""
        return self.get_full_name() or self.username
    
    @property
    def is_admin(self):
        """Verifica se é administrador"""
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_manager(self):
        """Verifica se é gerente"""
        return self.role in ['admin', 'manager']
    
    @property
    def is_professional(self):
        """Verifica se é profissional"""
        return self.role == 'professional'
    
    def update_last_access(self):
        """Atualiza timestamp do último acesso"""
        self.last_access = timezone.now()
        self.save(update_fields=['last_access'])
    
    def get_whatsapp_link(self):
        """Gera link do WhatsApp"""
        if self.mobile:
            number = ''.join(filter(str.isdigit, self.mobile))
            return f"https://wa.me/55{number}"
        return None


class UserProfile(models.Model):
    """
    Perfil estendido do usuário para informações adicionais.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )
    
    # Endereço
    address = models.CharField('Endereço', max_length=255, blank=True)
    address_number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=100, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('UF', max_length=2, blank=True)
    zip_code = models.CharField('CEP', max_length=10, blank=True)
    
    # Configurações
    receive_newsletter = models.BooleanField('Receber newsletter', default=True)
    receive_notifications = models.BooleanField('Receber notificações', default=True)
    
    # Avatar
    avatar = models.ImageField(
        'Avatar',
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"Perfil de {self.user.full_name}"