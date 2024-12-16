from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from perfil_profissional.models import PerfilProfissional
from perfil_profissional.api.serializers import PerfilProfissionalSerializer
from perfil_profissional.api.permissions import IsOwnerOrReadOnly


class PerfilProfissionalViewSet(viewsets.ModelViewSet):
    queryset = PerfilProfissional.objects.all()
    serializer_class = PerfilProfissionalSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]


    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            raise ValidationError({"detail": f"Erro ao criar perfil: {e}"})


    @action(detail=False, methods=['get'])
    def meu_perfil(self, request):
        # Rota customizada para listar o perfil do usuário autenticado
        perfil = self.get_queryset().select_related('endereco').filter(user=request.user).first()
        if not perfil:
            return Response({"detail": "Nenhum perfil encontrado."}, status=404)
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)

    
    @action(detail=True, methods=['patch'], url_path='atualizar-endereco')
    def atualizar_endereco(self, request, pk=None):
        perfil = self.get_object()
        endereco_serializer = EnderecoSerializer(perfil.endereco, data=request.data, partial=True)
        if endereco_serializer.is_valid():
            endereco_serializer.save()
            return Response(endereco_serializer.data)
        return Response(endereco_serializer.errors, status=400)

