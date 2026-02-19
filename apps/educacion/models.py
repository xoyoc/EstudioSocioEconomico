from django.db import models

from apps.configuracion.models import TimestampModel
from apps.personas.models import Persona

class NivelEducativo(models.Model):
    """Catálogo de niveles educativos"""
    nivel = models.CharField(max_length=100)
    orden = models.IntegerField(unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Niveles educativos"
        ordering = ['orden']

    def __str__(self):
        return self.nivel

class Educacion(TimestampModel):
    """Modelo de formación educativa"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='educacion')
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT)

    institucion = models.CharField(max_length=200)
    titulo = models.CharField(max_length=200)

    ESTADO_EDUCATIVO = [
        ('INC', 'Incompleto'),
        ('COM', 'Completo'),
        ('TRU', 'Trunco'),
        ('CUR', 'Cursando'),
    ]
    estado = models.CharField(max_length=3, choices=ESTADO_EDUCATIVO)

    anio_inicio = models.IntegerField()
    anio_fin = models.IntegerField(null=True, blank=True)

    tiene_cedula = models.BooleanField(default=False)
    numero_cedula = models.CharField(max_length=20, blank=True)

    documento_verificado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Educación"
        ordering = ['-anio_fin', '-anio_inicio']

    def __str__(self):
        return f"{self.nivel} - {self.institucion}"