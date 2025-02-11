from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.models import User, Subscription, Plan
from django.utils.timezone import now
from datetime import timedelta
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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]  # Permite acesso público para listar e visualizar planos

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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_subscription(self, request):
        """
        Cria uma assinatura para o usuário autenticado após o pagamento ser confirmado.
        """
        plan_id = request.data.get('plan_id')

        try:
            plan = Plan.objects.get(id=plan_id)
            user = request.user

            # Verifica se já existe uma assinatura ativa
            existing_subscription = Subscription.objects.filter(user=user, active=True).first()
            if existing_subscription:
                return Response({"error": "O usuário já possui uma assinatura ativa."}, status=status.HTTP_400_BAD_REQUEST)

            # Calcula a data de término da assinatura
            end_date = now() + timedelta(days=plan.duration_in_days)

            # Cria a assinatura
            subscription = Subscription.objects.create(
                user=user,
                start_date=now(),
                end_date=end_date,
                active=True
            )

            return Response({"message": "Assinatura criada com sucesso!", "subscription_id": subscription.id}, status=status.HTTP_201_CREATED)

        except Plan.DoesNotExist:
            return Response({"error": "Plano não encontrado."}, status=status.HTTP_404_NOT_FOUND)