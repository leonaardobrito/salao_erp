# apps/customers/models.py
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class Customer(BaseModel):
    """
    Cliente do salão.
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )

    name = models.CharField('Nome', max_length=255)
    email = models.EmailField('E-mail', blank=True, null=True)
    phone = models.CharField(
        'Telefone',
        max_length=20,
        validators=[phone_regex],
        blank=True,
        null=True
    )
    document = models.CharField('CPF/CNPJ', max_length=20, blank=True, null=True)

    # Endereço
    address = models.CharField('Endereço', max_length=255, blank=True)
    address_number = models.CharField('Número', max_length=20, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('UF', max_length=2, blank=True)
    zip_code = models.CharField('CEP', max_length=10, blank=True)

    notes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['document']),
        ]

    def __str__(self):
        return self.name
