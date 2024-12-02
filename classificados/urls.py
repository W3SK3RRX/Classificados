from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from perfil_profissional.api.viewsets import PerfilProfissionalViewSet


router = DefaultRouter()
router.register(r'perfis', PerfilProfissionalViewSet, basename='perfilprofissional')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('perfil-profissional/', include('perfil_profissional.urls')),
    path('', include(router.urls)),  # Inclui as rotas do roteador
]
