from django.urls import path
from .views import CriarPerfilProfissionalView

urlpatterns = [
    # Outras rotas
    path('criar-perfil-profissional/', CriarPerfilProfissionalView.as_view(), name='criar_perfil_profissional'),
]