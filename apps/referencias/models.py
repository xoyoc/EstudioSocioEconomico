from django.core.validators import MinValueValidator
from django.db import models

from apps.configuracion.models import TimestampModel
from apps.personas.models import Persona

class Referencia(TimestampModel):
    """Modelo de referencias personales, laborales y vecinales"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='referencias')

    TIPO_REFERENCIA = [
        ('PER', 'Personal'),
        ('LAB', 'Laboral'),
        ('VEC', 'Vecinal'),
        ('FAM', 'Familiar'),
        ('COM', 'Comercial'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPO_REFERENCIA)

    nombre = models.CharField(max_length=300)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    parentesco_o_relacion = models.CharField(max_length=100)
    tiempo_conocer_anios = models.IntegerField(validators=[MinValueValidator(0)])

    domicilio = models.TextField(blank=True)

    verificada = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    comentarios_verificacion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Referencias"

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"
