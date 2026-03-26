# apps/inventory/models.py
from django.db import models
from apps.core.models import BaseModel


class Stock(BaseModel):
    """
    Estoque de um produto.
    Uma entrada por produto.
    """
    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='stock',
        verbose_name='Produto'
    )
    quantity = models.IntegerField(
        'Quantidade',
        default=0,
        help_text='Quantidade em estoque'
    )
    min_quantity = models.IntegerField(
        'Quantidade mínima',
        default=0,
        blank=True,
        help_text='Alerta quando estoque estiver abaixo'
    )

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"

    @property
    def is_low_stock(self):
        return self.min_quantity > 0 and self.quantity <= self.min_quantity


class InventoryMovement(BaseModel):
    """
    Movimentação de estoque (entrada/saída/ajuste).
    """
    TYPE_CHOICES = [
        ('in', 'Entrada'),
        ('out', 'Saída'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name='Produto'
    )
    quantity = models.IntegerField(
        'Quantidade',
        help_text='Positivo para entrada, negativo para saída'
    )
    movement_type = models.CharField(
        'Tipo',
        max_length=20,
        choices=TYPE_CHOICES
    )
    notes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product.name}: {self.quantity:+d} ({self.get_movement_type_display()})"
