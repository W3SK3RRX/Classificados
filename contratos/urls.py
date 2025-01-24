from rest_framework.routers import DefaultRouter
from django.urls import path, include
from contratos.api.viewsets import ContratoViewSet
from contratos.views import ContratoAssinaturaAPIView

# Configuração do router existente
router = DefaultRouter()
router.register('', ContratoViewSet, basename='contrato')

# Adicionando o endpoint personalizado para assinatura
urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas do ViewSet
    path('<int:contrato_id>/assinatura/', ContratoAssinaturaAPIView.as_view(), name='contrato-assinatura'),
]
