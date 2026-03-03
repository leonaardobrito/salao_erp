from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permite acesso apenas a administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite acesso se for o proprietário do objeto ou admin.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin tem acesso a tudo
        if request.user.is_admin:
            return True
        
        # Verificar se é o proprietário (assumindo que obj tem atributo 'user' ou 'id')
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        
        return False


class IsProfessional(permissions.BasePermission):
    """
    Permite acesso apenas a profissionais.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_professional
