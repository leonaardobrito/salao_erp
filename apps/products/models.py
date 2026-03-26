# apps/products/models.py
from django.db import models
from decimal import Decimal
from apps.core.models import BaseModel


class Product(BaseModel):
    """
    Produto do salão (venda ou uso interno).
    """
    name = models.CharField('Nome', max_length=255)
    sku = models.CharField(
        'SKU/Código',
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    description = models.TextField('Descrição', blank=True)
    unit_price = models.DecimalField(
        'Preço unitário',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    cost_price = models.DecimalField(
        'Preço de custo',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        blank=True
    )
    category = models.CharField(
        'Categoria',
        max_length=100,
        blank=True,
        help_text='Ex: Shampoo, Tintura, Acessórios'
    )
    unit = models.CharField(
        'Unidade',
        max_length=20,
        default='un',
        help_text='Ex: un, kg, ml'
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - R$ {self.unit_price}"
