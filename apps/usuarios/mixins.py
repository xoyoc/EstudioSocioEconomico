"""
Mixins de control de acceso basado en roles (ANA / INS).

Uso en vistas:
    class MiVistaPrivada(AnalistaRequeridoMixin, DetailView):
        ...
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RolRequeridoMixin(LoginRequiredMixin):
    """
    Mixin base. Subclases deben definir `roles_permitidos` como
    una lista/tupla de códigos de rol, p.ej. ['ANA'] o ['ANA', 'INS'].
    """
    roles_permitidos = []

    def dispatch(self, request, *args, **kwargs):
        respuesta = super().dispatch(request, *args, **kwargs)
        # super() redirige si no está autenticado; solo llegar aquí si sí lo está
        if not request.user.is_authenticated:
            return respuesta

        # Superusuarios siempre tienen acceso
        if request.user.is_superuser:
            return respuesta

        try:
            rol = request.user.perfil.rol
        except Exception:
            raise PermissionDenied

        if rol not in self.roles_permitidos:
            raise PermissionDenied

        return respuesta


class AnalistaRequeridoMixin(RolRequeridoMixin):
    """Solo analistas (ANA) pueden acceder."""
    roles_permitidos = ['ANA']


class InspectorRequeridoMixin(RolRequeridoMixin):
    """Analistas e inspectores pueden acceder."""
    roles_permitidos = ['ANA', 'INS']
