from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from perfil_profissional.models import PerfilProfissional
from perfil_profissional.api.serializers import PerfilProfissionalSerializer, PerfilProfissionalResumoSerializer, EnderecoSerializer
from perfil_profissional.api.permissions import IsOwnerOrReadOnly


class PerfilProfissionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Perfis Profissionais.
    Inclui listagem resumida, detalhes completos, e ações customizadas.
    """
    queryset = PerfilProfissional.objects.select_related('endereco').all()

    def get_serializer_class(self):
        # Usa o serializer resumido para listagem e o completo para outras ações
        if self.action == 'list':
            return PerfilProfissionalResumoSerializer
        return PerfilProfissionalSerializer

    def get_permissions(self):
        # Permissões diferentes para ações específicas
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        """
        Sobrescreve o método para associar o perfil ao usuário autenticado.
        """
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            raise ValidationError({"detail": f"Erro ao criar perfil: {e}"})

    @action(detail=False, methods=['get'])
    def meu_perfil(self, request):
        """
        Rota customizada para retornar o perfil do usuário autenticado.
        """
        try:
            perfil = self.get_queryset().get(user=request.user)
        except PerfilProfissional.DoesNotExist:
            return Response({"detail": "Nenhum perfil encontrado."}, status=404)

        serializer = self.get_serializer(perfil)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='atualizar-endereco')
    def atualizar_endereco(self, request, pk=None):
        """
        Rota customizada para atualizar o endereço do perfil.
        """
        perfil = self.get_object()
        endereco_serializer = EnderecoSerializer(perfil.endereco, data=request.data, partial=True)
        if endereco_serializer.is_valid():
            endereco_serializer.save()
            return Response(endereco_serializer.data)
        return Response(endereco_serializer.errors, status=400)
