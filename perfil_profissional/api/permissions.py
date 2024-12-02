from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir apenas ao dono do perfil editar ou deletar.
    """
    def has_object_permission(self, request, view, obj):
        # Permite leitura para qualquer pessoa
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite edição apenas se o usuário for o dono
        return obj.user == request.user
