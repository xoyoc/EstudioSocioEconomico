"""
Señales para creación automática de notificaciones al cambiar el estado de un estudio.

Disparadores:
  - pre_save: captura el estado anterior antes de guardar
  - post_save: detecta el cambio de estado y crea notificaciones
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.estudios.models import EstudioSocioeconomico
from .models import Notificacion


# Mensajes por estado destino: (tipo, título, prioridad)
_CONFIG_ESTADO = {
    'VIS': ('VIS', 'Visita programada', 'MED'),
    'PRO': ('PRO', 'Estudio en proceso', 'MED'),
    'COM': ('PRO', 'Estudio completado', 'MED'),
    'REV': ('PRO', 'Estudio enviado a revisión', 'MED'),
    'APR': ('APR', 'Estudio aprobado', 'ALT'),
    'REC': ('REC', 'Estudio rechazado', 'ALT'),
    'CAN': ('SIS', 'Estudio cancelado', 'ALT'),
}


def _usuarios_a_notificar(estudio, nuevo_estado):
    """
    Devuelve el conjunto de usuarios que deben recibir la notificación
    dependiendo del estado de destino.
    """
    usuarios = set()

    # Siempre notificar al creador del estudio
    if estudio.created_by_id:
        usuarios.add(estudio.created_by_id)

    # En aprobación/rechazo también notificar a los staff activos
    if nuevo_estado in ('APR', 'REC', 'CAN'):
        staff_ids = (
            User.objects
            .filter(is_staff=True, is_active=True)
            .values_list('pk', flat=True)
        )
        usuarios.update(staff_ids)

    return usuarios


def _construir_mensaje(estudio, nuevo_estado):
    """Genera el mensaje descriptivo de la notificación."""
    persona = estudio.persona
    nombre = persona.nombre_completo if hasattr(persona, 'nombre_completo') else str(persona)

    mensajes = {
        'VIS': f'Se ha programado una visita para el estudio de {nombre} (folio: {estudio.persona.folio}).',
        'PRO': f'El estudio de {nombre} ha iniciado el proceso de análisis.',
        'COM': f'El estudio de {nombre} ha sido marcado como completado y está listo para revisión.',
        'REV': f'El estudio de {nombre} fue enviado a revisión por un analista senior.',
        'APR': f'El estudio socioeconómico de {nombre} ha sido APROBADO.',
        'REC': f'El estudio socioeconómico de {nombre} ha sido RECHAZADO. Revisa la conclusión del expediente.',
        'CAN': f'El estudio de {nombre} ha sido cancelado.',
    }
    return mensajes.get(nuevo_estado, f'El estado del estudio de {nombre} cambió a {nuevo_estado}.')


@receiver(pre_save, sender=EstudioSocioeconomico)
def _capturar_estado_anterior(sender, instance, **kwargs):
    """Guarda el estado actual en un atributo temporal antes del guardado."""
    if instance.pk:
        try:
            instance._estado_anterior = (
                EstudioSocioeconomico.objects
                .values_list('estado', flat=True)
                .get(pk=instance.pk)
            )
        except EstudioSocioeconomico.DoesNotExist:
            instance._estado_anterior = None
    else:
        instance._estado_anterior = None


@receiver(post_save, sender=EstudioSocioeconomico)
def _notificar_cambio_estado(sender, instance, created, **kwargs):
    """Crea notificaciones cuando el estado del estudio cambia."""
    if created:
        return

    estado_anterior = getattr(instance, '_estado_anterior', None)
    nuevo_estado = instance.estado

    if estado_anterior is None or estado_anterior == nuevo_estado:
        return

    config = _CONFIG_ESTADO.get(nuevo_estado)
    if not config:
        return

    tipo, titulo, prioridad = config
    mensaje = _construir_mensaje(instance, nuevo_estado)
    usuario_ids = _usuarios_a_notificar(instance, nuevo_estado)

    notificaciones = [
        Notificacion(
            usuario_id=uid,
            estudio=instance,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            prioridad=prioridad,
        )
        for uid in usuario_ids
    ]
    if notificaciones:
        Notificacion.objects.bulk_create(notificaciones)
