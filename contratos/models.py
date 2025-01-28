from django.db import models
from django.conf import settings
from perfil_profissional.models import PerfilProfissional
from weasyprint import HTML
import os


class ContratoTemplate(models.Model):
    nome = models.CharField(max_length=255)
    conteudo = models.TextField()
    padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


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
    template = models.ForeignKey(
        ContratoTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos'
    )  # Template utilizado
    conteudo_personalizado = models.TextField(
        null=True,
        blank=True
    )  # Personalização opcional
    descricao = models.TextField()  # Descrição do serviço ou objeto do contrato
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    prazo_execucao = models.DateField()  # Prazo de execução do serviço
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    contrato_gerado = models.FileField(upload_to='contratos/gerados/', blank=True, null=True)
    contrato_assinado = models.FileField(upload_to='contratos/assinados/', blank=True, null=True)

    def gerar_contrato(self):
        """
        Gera o conteúdo final do contrato, substituindo placeholders com os dados do contrato.
        """
        # Usa o conteúdo personalizado ou o template associado
        conteudo = self.conteudo_personalizado or (self.template.conteudo if self.template else "")
        placeholders = {
            "{{contratante_nome}}": self.contratante.get_full_name(),
            "{{contratado_nome}}": self.contratado.usuario.get_full_name(),
            "{{descricao}}": self.descricao,
            "{{valor}}": f"R$ {self.valor:.2f}",
            "{{prazo_execucao}}": self.prazo_execucao.strftime("%d/%m/%Y"),
            "{{data}}": self.criado_em.strftime("%d/%m/%Y"),
        }
        for key, value in placeholders.items():
            conteudo = conteudo.replace(key, value)
        return conteudo
    
    def salvar_contrato_pdf(self):
        """
        Gera o PDF do contrato e salva no campo `contrato_gerado`.
        """
        conteudo_final = self.gerar_contrato()
        caminho_diretorio = 'media/contratos/gerados/'
        os.makedirs(caminho_diretorio, exist_ok=True)  # Garante que o diretório exista

        caminho_arquivo = f'{caminho_diretorio}contrato_{self.id}.pdf'

        # Gera o PDF
        html = HTML(string=conteudo_final)
        html.write_pdf(caminho_arquivo)

        # Salva o caminho no campo `contrato_gerado`
        self.contrato_gerado = caminho_arquivo
        self.save()


    def titulo(self):
        return f"Contrato {self.id} - {self.contratante.get_full_name()}"

    def __str__(self):
        return self.titulo()
   