# apps/services/models.py
from django.db import models
from decimal import Decimal
from apps.core.models import BaseModel


class Service(BaseModel):
    """
    Serviço oferecido pelo salão.
    """
    name = models.CharField('Nome', max_length=255)
    description = models.TextField('Descrição', blank=True)
    duration_minutes = models.PositiveIntegerField(
        'Duração (minutos)',
        default=60,
        help_text='Duração estimada do serviço em minutos'
    )
    price = models.DecimalField(
        'Preço',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    category = models.CharField(
        'Categoria',
        max_length=100,
        blank=True,
        help_text='Ex: Cabelo, Unhas, Maquiagem'
    )

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - R$ {self.price}"
