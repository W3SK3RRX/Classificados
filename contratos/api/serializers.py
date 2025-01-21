from rest_framework import serializers
from contratos.models import Contrato

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'
        read_only_fields = ['status', 'criado_em', 'atualizado_em']

class ContratoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = ['status', 'contrato_assinado']
        read_only_fields = ['contratante', 'contratado', 'descricao', 'valor', 'prazo_execucao']
