# apps/professionals/models.py
from django.db import models
from apps.core.models import BaseModel


class Professional(BaseModel):
    """
    Perfil profissional vinculado a um usuário.
    Estende dados do User com informações específicas do salão.
    """
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='professional_profile',
        verbose_name='Usuário'
    )
    commission_percent = models.DecimalField(
        'Comissão (%)',
        max_digits=5,
        decimal_places=2,
        default=0,
        blank=True
    )
    color = models.CharField(
        'Cor (agenda)',
        max_length=7,
        default='#3498db',
        help_text='Cor em hexadecimal para exibição na agenda'
    )
    specialties = models.CharField(
        'Especialidades',
        max_length=255,
        blank=True,
        help_text='Ex: Corte, Coloração, Manicure'
    )

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        ordering = ['user__first_name']

    def __str__(self):
        return self.user.full_name

    @property
    def name(self):
        return self.user.full_name
