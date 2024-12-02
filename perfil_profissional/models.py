from django.db import models
from django.conf import settings  # Para acessar o modelo User customizado

class PerfilProfissional(models.Model):
    TIPO_CHOICES = [
        ('profissional', 'Profissional Liberal'),
        ('empresa', 'Empresa'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    foto_logo = models.ImageField(upload_to='uploads/fotos_perfil/', blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)  # Apenas para profissionais
    cnpj = models.CharField(max_length=18, blank=True, null=True)  # Apenas para empresas
    endereco = models.JSONField()  # Para armazenar endereço de forma compacta (ou use um modelo relacionado)
    telefone = models.CharField(max_length=15)
    area_atuacao = models.CharField(max_length=200)
    biografia = models.TextField(blank=True, null=True)
    certificados = models.FileField(upload_to='uploads/certificados/', blank=True, null=True)
    registros_profissionais = models.FileField(upload_to='uploads/registros_profissionais/', blank=True, null=True)
    concordou_termos = models.BooleanField(default=False)  # Campo para salvar a resposta do usuário

    def __str__(self):
        return f"{self.user.email} - {self.get_tipo_display()}"