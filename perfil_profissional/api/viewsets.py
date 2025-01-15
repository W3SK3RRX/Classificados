from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from perfil_profissional.models import PerfilProfissional
from .serializers import PerfilProfissionalSerializer

# Listar todos os perfis (Profissionais e Empresas) - Página Inicial
class PerfilProfissionalListView(generics.ListAPIView):
    queryset = PerfilProfissional.objects.select_related('user', 'endereco').all()
    serializer_class = PerfilProfissionalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['area_atuacao', 'endereco__cidade', 'endereco__estado']
    search_fields = ['profile_name', 'area_atuacao']
    ordering_fields = ['profile_name', 'area_atuacao']

# Criar um novo perfil
class PerfilProfissionalCreateView(generics.CreateAPIView):
    queryset = PerfilProfissional.objects.all()
    serializer_class = PerfilProfissionalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Detalhar um perfil específico
class PerfilProfissionalDetailView(generics.RetrieveAPIView):
    queryset = PerfilProfissional.objects.select_related('user', 'endereco').all()
    serializer_class = PerfilProfissionalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Atualizar um perfil específico
class PerfilProfissionalUpdateView(generics.UpdateAPIView):
    queryset = PerfilProfissional.objects.select_related('user', 'endereco').all()
    serializer_class = PerfilProfissionalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Excluir um perfil específico
class PerfilProfissionalDeleteView(generics.DestroyAPIView):
    queryset = PerfilProfissional.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
