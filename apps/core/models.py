from django.db import models

class BaseModel(models.Model):
    """Modelo base abstrato com campos comuns"""
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}"