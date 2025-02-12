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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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
        return [AllowAny()]

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

            existing_subscription = Subscription.objects.filter(user=user, active=True).first()
            if existing_subscription:
                return Response({"error": "O usuário já possui uma assinatura ativa."}, status=status.HTTP_400_BAD_REQUEST)

            end_date = now() + timedelta(days=plan.duration_in_days)

            subscription = Subscription.objects.create(
                user=user,
                start_date=now(),
                end_date=end_date,
                active=False,  # Inicialmente inativa
                payment_confirmed=False  # Inicialmente o pagamento não foi confirmado
            )

            return Response({"message": "Assinatura criada com sucesso, aguardando confirmação de pagamento.", "subscription_id": subscription.id}, status=status.HTTP_201_CREATED)

        except Plan.DoesNotExist:
            return Response({"error": "Plano não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm_payment(self, request, pk=None):
        """
        Confirma o pagamento de uma assinatura e a torna ativa, se válido.
        """
        subscription = self.get_object()

        # Verifica se a assinatura já foi confirmada
        if subscription.payment_confirmed:
            return Response({"error": "Pagamento já confirmado."}, status=status.HTTP_400_BAD_REQUEST)

        # Marca o pagamento como confirmado e atualiza a assinatura
        subscription.payment_confirmed = True
        subscription.save()

        return Response({"message": "Pagamento confirmado e assinatura ativada com sucesso!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscription_status(self, request):
        """
        Endpoint para verificar o status da assinatura do usuário.
        """
        user = request.user
        active_subscription = Subscription.objects.filter(user=user, active=True).first()

        if active_subscription:
            return Response({
                "active": True,
                "start_date": active_subscription.start_date,
                "end_date": active_subscription.end_date
            })
        
        # Se não houver assinatura ativa
        return Response({"active": False})
