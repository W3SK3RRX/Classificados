from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.models import User, Subscription, Plan
from .serializers import (
    UserWithSubscriptionCreationSerializer,
    UserWithSubscriptionSerializer,
    PlanSerializer,
    SubscriptionSerializer
)

class UserViewSet(ModelViewSet):
    """
    ViewSet para gerenciar usuários.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserWithSubscriptionCreationSerializer
        return UserWithSubscriptionSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Endpoint para retornar os dados do usuário autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class PlanViewSet(ModelViewSet):
    """
    ViewSet para gerenciar planos.
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Somente usuários admin podem criar planos.
        """
        if not request.user.is_staff:
            return Response({"detail": "Você não tem permissão para criar planos."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SubscriptionViewSet(ModelViewSet):
    """
    ViewSet para gerenciar assinaturas.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Usuários só podem ver suas próprias assinaturas, exceto admins.
        """
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return self.queryset.filter(user=user)
