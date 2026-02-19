from django.db import models

from apps.configuracion.models import TimestampModel
from apps.personas.models import Persona

class HistorialLaboral(TimestampModel):
    """Modelo de historial laboral"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='historial_laboral')

    empresa = models.CharField(max_length=200)
    puesto = models.CharField(max_length=200)
    telefono_empresa = models.CharField(max_length=15)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    es_trabajo_actual = models.BooleanField(default=False)

    salario_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    salario_final = models.DecimalField(max_digits=10, decimal_places=2)

    nombre_jefe = models.CharField(max_length=200)
    telefono_jefe = models.CharField(max_length=15)

    motivo_separacion = models.TextField(blank=True)
    verificada = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Historiales laborales"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.empresa} - {self.puesto}"
