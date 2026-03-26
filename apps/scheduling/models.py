# apps/scheduling/models.py
from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel


class Appointment(BaseModel):
    """
    Agendamento de atendimento.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('confirmed', 'Confirmado'),
        ('in_progress', 'Em atendimento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('no_show', 'Não compareceu'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Cliente'
    )
    professional = models.ForeignKey(
        'professionals.Professional',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Profissional'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Serviço'
    )
    scheduled_at = models.DateTimeField('Data/Hora agendada')
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['scheduled_at']),
            models.Index(fields=['status']),
            models.Index(fields=['professional']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.professional.name} em {self.scheduled_at}"
