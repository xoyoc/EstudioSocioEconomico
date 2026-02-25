from .models import Notificacion


def notif_count(request):
    """
    Inyecta `notif_count_global` en todos los templates.
    Retorna 0 si el usuario no está autenticado.
    """
    if not request.user.is_authenticated:
        return {'notif_count_global': 0}
    count = Notificacion.objects.filter(
        usuario=request.user, leida=False
    ).count()
    return {'notif_count_global': count}
