from django.db import models

from apps.configuracion.models import TimestampModel, TipoEstudio
from apps.personas.models import Persona

class EstudioSocioeconomico(TimestampModel):
    """Modelo principal del estudio socioeconómico"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='estudios')
    tipo_estudio = models.ForeignKey(TipoEstudio, on_delete=models.PROTECT)

    ESTADO_ESTUDIO = [
        ('BOR', 'Borrador'),
        ('VIS', 'Visita programada'),
        ('PRO', 'En proceso'),
        ('COM', 'Completado'),
        ('REV', 'En revisión'),
        ('APR', 'Aprobado'),
        ('REC', 'Rechazado'),
        ('CAN', 'Cancelado'),
    ]
    estado = models.CharField(max_length=3, choices=ESTADO_ESTUDIO, default='BOR')

    fecha_programada_visita = models.DateTimeField(null=True, blank=True)
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    observaciones = models.TextField(blank=True)
    conclusion = models.TextField(blank=True)
    puntuacion_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Estudios socioeconómicos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Estudio {self.persona.folio} - {self.get_estado_display()}"
