from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from perfil_profissional.api.serializers import PerfilProfissionalSerializer

class CriarPerfilProfissionalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PerfilProfissionalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Perfil criado com sucesso.", "perfil": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
