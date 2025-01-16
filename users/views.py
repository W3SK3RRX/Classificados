from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.api.serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    """
    Endpoint para login de usuários usando JWT.
    """
    def post(self, request, *args, **kwargs):
        print("Endpoint de login acessado")
        email = request.data.get("email")
        password = request.data.get("password")

        # Verifica se o usuário existe
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se a senha está correta
        if not user.check_password(password):
            return Response({"error": "Senha incorreta"}, status=status.HTTP_401_UNAUTHORIZED)

        # Autentica o usuário
        user = authenticate(email=email, password=password)
        if user:
            # Gera os tokens de autenticação
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "lastname": user.lastname,
                    "email": user.email,
                    "user_type": user.user_type,  # Personalize conforme o modelo
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Erro de autenticação"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({"detail": "Token de refresh não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Criação do objeto RefreshToken a partir do refresh_token enviado
            token = RefreshToken(refresh_token)
            # Coloca o token de refresh na blacklist
            token.blacklist()
            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Trata exceções que podem ocorrer durante o processo de blacklisting
            return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "E-mail de redefinição de senha enviado com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
