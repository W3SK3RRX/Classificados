from rest_framework import serializers
from perfil_profissional.models import PerfilProfissional

class PerfilProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilProfissional
        fields = [
            'tipo', 'foto_logo', 'cpf', 'cnpj', 'endereco', 
            'telefone', 'area_atuacao', 'biografia', 
            'certificados', 'registros_profissionais', 'concordou_termos'
        ]

    def validate_concordou_termos(self, value):
        if not value:
            raise serializers.ValidationError("Você deve concordar com os termos para criar o perfil.")
        return value

    def validate(self, data):
        tipo = data.get('tipo')
        cpf = data.get('cpf')
        cnpj = data.get('cnpj')

        # Validação para garantir CPF/CNPJ conforme o tipo
        if tipo == 'profissional' and not cpf:
            raise serializers.ValidationError({"cpf": "CPF é obrigatório para profissionais liberais."})
        if tipo == 'empresa' and not cnpj:
            raise serializers.ValidationError({"cnpj": "CNPJ é obrigatório para empresas."})

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return PerfilProfissional.objects.create(user=user, **validated_data)