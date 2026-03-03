# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline para exibir perfil no admin"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuração do admin para User"""
    
    inlines = [UserProfileInline]
    
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'role', 'phone', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone', 'mobile', 'document', 'birth_date'
            )
        }),
        (_('Função'), {
            'fields': ('role', 'notes')
        }),
        (_('Controle'), {
            'fields': ('is_active', 'last_access', 'created_by')
        }),
        (_('Permissões'), {
            'fields': (
                'is_superuser', 'groups', 'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_('Datas Importantes'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'role'
            ),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'last_access']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para UserProfile"""
    
    list_display = ['user', 'city', 'state', 'receive_newsletter']
    list_filter = ['receive_newsletter', 'state']
    search_fields = ['user__username', 'user__email', 'city']
    raw_id_fields = ['user']