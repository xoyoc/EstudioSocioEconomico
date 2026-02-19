from django.contrib.auth.models import User
from django.db import models

from apps.configuracion.models import TimestampModel
from apps.estudios.models import EstudioSocioeconomico


class Notificacion(TimestampModel):
    """Modelo para notificaciones del sistema"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    estudio = models.ForeignKey(EstudioSocioeconomico, on_delete=models.CASCADE, null=True, blank=True)

    TIPO_NOTIFICACION = [
        ('PRO', 'Proceso'),
        ('VIS', 'Visita'),
        ('DOC', 'Documentos'),
        ('APR', 'Aprobación'),
        ('REC', 'Rechazo'),
        ('SIS', 'Sistema'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPO_NOTIFICACION)

    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()

    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    PRIORIDAD = [
        ('ALT', 'Alta'),
        ('MED', 'Media'),
        ('BAJ', 'Baja'),
    ]
    prioridad = models.CharField(max_length=3, choices=PRIORIDAD, default='MED')

    class Meta:
        verbose_name_plural = "Notificaciones"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"