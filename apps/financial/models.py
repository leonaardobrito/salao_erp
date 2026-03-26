# apps/financial/models.py
from django.db import models
from decimal import Decimal
from apps.core.models import BaseModel


class Transaction(BaseModel):
    """
    Transação financeira (receita ou despesa).
    """
    TYPE_CHOICES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Dinheiro'),
        ('card', 'Cartão'),
        ('pix', 'PIX'),
        ('transfer', 'Transferência'),
        ('other', 'Outro'),
    ]

    transaction_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES
    )
    amount = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2
    )
    description = models.CharField('Descrição', max_length=255)
    payment_method = models.CharField(
        'Forma de pagamento',
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash'
    )
    transaction_date = models.DateField('Data da transação')
    appointment = models.ForeignKey(
        'scheduling.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='Agendamento'
    )
    notes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['transaction_type']),
        ]

    def __str__(self):
        return f"{self.get_transaction_type_display()} - R$ {self.amount} - {self.description}"
