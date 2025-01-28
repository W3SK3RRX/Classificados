from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import models
from contratos.models import Contrato
from .serializers import ContratoSerializer, ContratoUpdateSerializer


class ContratoViewSet(ModelViewSet):
    """
    ViewSet para gerenciar contratos.
    """
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtra os contratos para que cada usuário veja apenas os seus.
        """
        user = self.request.user
        return Contrato.objects.filter(
            models.Q(contratante=user) | models.Q(contratado__user=user)
        )

    def perform_create(self, serializer):
        """
        Define o contratante automaticamente com base no usuário autenticado.
        """
        contrato = serializer.save(contratante=self.request.user)  # Salva o contrato
        contrato.salvar_contrato_pdf()  # Gera o PDF após a criação

    @action(detail=True, methods=['patch'], url_path='atualizar-status')
    def atualizar_status(self, request, pk=None):
        """
        Permite ao contratado atualizar o status e anexar o contrato assinado.
        """
        contrato = self.get_object()
        if contrato.contratado.user != request.user:
            return Response({"detail": "Você não tem permissão para atualizar este contrato."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ContratoUpdateSerializer(contrato, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
