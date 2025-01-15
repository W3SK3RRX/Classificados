from rest_framework import serializers
from perfil_profissional.models import PerfilProfissional, Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']

class PerfilProfissionalSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = PerfilProfissional
        fields = [
            'id', 'user', 'foto_logo', 'profile_name', 'cpf', 'cnpj', 'endereco', 
            'telefone', 'area_atuacao', 'biografia', 'certificados', 
            'registros_profissionais', 'concordou_termos'
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        return PerfilProfissional.objects.create(endereco=endereco, **validated_data)

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            for attr, value in endereco_data.items():
                setattr(instance.endereco, attr, value)
            instance.endereco.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
