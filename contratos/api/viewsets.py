from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import models
from contratos.models import Contrato
from .serializers import ContratoSerializer, ContratoUpdateSerializer
from django.shortcuts import get_object_or_404


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


    @action(detail=True, methods=['post'])
    def gerar_pdf(self, request, pk=None):
        """
        Gera o PDF do contrato e retorna a URL do arquivo gerado.
        """
        contrato = get_object_or_404(Contrato, pk=pk)
        
        try:
            contrato.salvar_contrato_pdf()
            return Response({"message": "PDF gerado com sucesso", "contrato_gerado": contrato.contrato_gerado.url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

