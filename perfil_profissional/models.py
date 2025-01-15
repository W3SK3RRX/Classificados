from django.db import models
from django.conf import settings  # Para acessar o modelo User customizado
from django.core.exceptions import ValidationError
import re

class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Ex.: 'SP', 'RJ'
    cep = models.CharField(max_length=9)  # Formato: '12345-678'

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"


class PerfilProfissional(models.Model):
    # Validators para CPF e CNPJ
    def validate_cpf(value):
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', value):
            raise ValidationError('CPF inválido. Formato esperado: 000.000.000-00')

    def validate_cnpj(value):
        if not re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', value):
            raise ValidationError('CNPJ inválido. Formato esperado: 00.000.000/0000-00')

    def validate_certificados(value):
        if value.size > 5 * 1024 * 1024:  # Limite de 5MB
            raise ValidationError("Certificado excede o tamanho máximo permitido de 5MB.")
        return value

    # Relação com o usuário
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Dados do perfil
    foto_logo = models.ImageField(upload_to='uploads/fotos_perfil/', blank=True, null=True)
    profile_name = models.CharField(max_length=40, blank=False, default="")  # Nome do profissional ou empresa
    cpf = models.CharField(
        unique=True,
        max_length=14,
        blank=True,
        null=True,
        validators=[validate_cpf],
        help_text="Obrigatório para profissionais liberais."
    )
    cnpj = models.CharField(
        unique=True,
        max_length=18,
        blank=True,
        null=True,
        validators=[validate_cnpj],
        help_text="Obrigatório para empresas."
    )
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, related_name="perfil_profissional")
    telefone = models.CharField(max_length=15)
    area_atuacao = models.CharField(max_length=200)
    biografia = models.TextField(blank=True, null=True)

    # Documentos e termos
    certificados = models.FileField(upload_to='uploads/certificados/', blank=True, null=True)
    registros_profissionais = models.FileField(upload_to='uploads/registros_profissionais/', blank=True, null=True)
    concordou_termos = models.BooleanField(default=True)

    def clean(self):
        # Regras de validação
        if self.user.user_type == settings.USER_TYPE_PROFESSIONAL and not self.cpf:
            raise ValidationError("CPF é obrigatório para profissionais liberais.")
        if self.user.user_type == settings.USER_TYPE_COMPANY and not self.cnpj:
            raise ValidationError("CNPJ é obrigatório para empresas.")

    def __str__(self):
        return f"{self.profile_name} ({self.get_user_type_display()})"
