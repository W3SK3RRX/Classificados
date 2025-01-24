from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contrato
from .services.d4sign import D4SignService

class ContratoAssinaturaAPIView(APIView):
    """
    Endpoint para enviar um contrato para assinatura via D4Sign.
    """
    def post(self, request, contrato_id):
        contrato = Contrato.objects.get(pk=contrato_id)
        if not contrato.contrato_gerado:
            return Response({"error": "Contrato PDF não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Defina o caminho do arquivo gerado
        file_path = contrato.contrato_gerado.path
        document_name = f"Contrato_{contrato.id}.pdf"

        # Enviar para o D4Sign
        try:
            document_response = D4SignService.create_document(file_path, document_name, safe_key='seu_safe_key')
            document_key = document_response['uuid']
            contrato.d4sign_document_key = document_key
            contrato.save()

            # Adicionar signatários
            signers = [
                {
                    "email": contrato.contratante.email,
                    "act": "1",  # Tipo de assinatura
                    "foreign": "0"  # Assinatura local
                },
                {
                    "email": contrato.contratado.user.email,
                    "act": "1",
                    "foreign": "0"
                }
            ]
            signer_response = D4SignService.add_signers(document_key, signers)

            return Response({"detail": "Contrato enviado para assinatura.", "document_key": document_key})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
