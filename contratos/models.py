from django.db import models
from django.conf import settings
from perfil_profissional.models import PerfilProfissional

class Contrato(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('assinatura', 'Em Assinatura'),
        ('concluido', 'Concluído'),
        ('arquivado', 'Arquivado'),
    ]

    contratante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contratos_contratante'
    )
    contratado = models.ForeignKey(
        PerfilProfissional,
        on_delete=models.CASCADE,
        related_name='contratos_contratado'
    )
    descricao = models.TextField()  # Descrição do serviço ou objeto do contrato
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    prazo_execucao = models.DateField()  # Prazo de execução do serviço
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    contrato_gerado = models.FileField(upload_to='contratos/gerados/', blank=True, null=True)
    contrato_assinado = models.FileField(upload_to='contratos/assinados/', blank=True, null=True)

    def __str__(self):
        return f"Contrato #{self.id} - {self.status}"
