from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from perfil_profissional.api.viewsets import PerfilProfissionalViewSet
from users.api.viewsets import UserViewSet, PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('plans', PlanViewSet, basename='plan')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')

#router = DefaultRouter()
#router.register(r'perfis', PerfilProfissionalViewSet, basename='perfilprofissional')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('users/', include('users.urls')),
    #path('perfil-profissional/', include('perfil_profissional.urls')),
    path('', include(router.urls)),  # Inclui as rotas do roteador
]
