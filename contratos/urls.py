from rest_framework.routers import DefaultRouter
from contratos.api.viewsets import ContratoViewSet

router = DefaultRouter()
router.register('', ContratoViewSet, basename='contrato')

urlpatterns = router.urls
