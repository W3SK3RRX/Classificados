from django.urls import path
from perfil_profissional.api.viewsets import (
    PerfilProfissionalListView,
    PerfilProfissionalCreateView,
    PerfilProfissionalDetailView,
    PerfilProfissionalUpdateView,
    PerfilProfissionalDeleteView,
)

urlpatterns = [
    path('', PerfilProfissionalListView.as_view(), name='perfil-list'),
    path('criar/', PerfilProfissionalCreateView.as_view(), name='perfil-create'),
    path('<int:pk>/', PerfilProfissionalDetailView.as_view(), name='perfil-detail'),
    path('<int:pk>/editar/', PerfilProfissionalUpdateView.as_view(), name='perfil-update'),
    path('<int:pk>/excluir/', PerfilProfissionalDeleteView.as_view(), name='perfil-delete'),
]
