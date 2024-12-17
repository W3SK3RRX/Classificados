from rest_framework import serializers
from perfil_profissional.models import PerfilProfissional, Endereco


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']


class PerfilProfissionalSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()  # Aninhando o serializador de Endereco

    class Meta:
        model = PerfilProfissional
        fields = [
            'tipo', 'foto_logo', 'profile_name', 'cpf', 'cnpj', 'endereco',
            'telefone', 'area_atuacao', 'biografia',
            'certificados', 'registros_profissionais', 'concordou_termos'
        ]

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        user = self.context['request'].user
        return PerfilProfissional.objects.create(user=user, endereco=endereco, **validated_data)

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            for attr, value in endereco_data.items():
                setattr(instance.endereco, attr, value)
            instance.endereco.save(update_fields=endereco_data.keys())

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
# serializers.py
class PerfilProfissionalResumoSerializer(serializers.ModelSerializer):
    cidade = serializers.CharField(source='endereco.cidade')
    estado = serializers.CharField(source='endereco.estado')

    class Meta:
        model = PerfilProfissional
        fields = ['id', 'foto_logo', 'profile_name', 'cidade', 'estado', 'tipo']
