from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.viewsets import UserViewSet, PlanViewSet, SubscriptionViewSet
from contratos.api.viewsets import ContratoViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('plans', PlanViewSet, basename='plan')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('contratos', ContratoViewSet, basename='contract')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Rotas adicionais de `users`
    path('', include(router.urls)),  # Rotas de `viewsets`
    path('perfil-profissional/', include('perfil_profissional.urls')),
]

