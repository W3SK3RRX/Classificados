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
        """
        Define permissões diferentes para métodos de leitura e escrita.
        """
        if self.action in ['list', 'retrieve']:  # Permite acesso público a GET (list e retrieve)
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]  # Exige autenticação para POST, PUT, PATCH, DELETE

    def perform_create(self, serializer):
        # Associa o perfil ao usuário autenticado automaticamente
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def meu_perfil(self, request):
        # Rota customizada para listar o perfil do usuário autenticado
        perfil = self.get_queryset().filter(user=request.user).first()
        if not perfil:
            return Response({"detail": "Nenhum perfil encontrado."}, status=404)
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)
