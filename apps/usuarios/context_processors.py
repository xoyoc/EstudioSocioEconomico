from .models import PerfilUsuario


def perfil_usuario(request):
    """
    Inyecta `perfil_usuario` y `es_analista` / `es_inspector` en todos los templates.
    """
    if not request.user.is_authenticated:
        return {
            'perfil_usuario': None,
            'es_analista': False,
            'es_inspector': False,
        }
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None

    return {
        'perfil_usuario': perfil,
        'es_analista': perfil.es_analista if perfil else False,
        'es_inspector': perfil.es_inspector if perfil else False,
    }
