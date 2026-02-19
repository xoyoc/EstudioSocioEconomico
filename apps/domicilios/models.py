from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.configuracion.models import TimestampModel
from apps.personas.models import Persona

# Create your models here.
class Domicilio(TimestampModel):
    """Modelo de domicilio - Una persona puede tener múltiples domicilios"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='domicilios')

    TIPO_DOMICILIO = [
        ('ACT', 'Actual'),
        ('ANT', 'Anterior'),
        ('REF', 'Referencia'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPO_DOMICILIO, default='ACT')

    # Dirección
    calle = models.CharField(max_length=200)
    numero_exterior = models.CharField(max_length=20)
    numero_interior = models.CharField(max_length=20, blank=True)
    entre_calles = models.CharField(max_length=200, blank=True)
    colonia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='México')

    # Características de la vivienda
    TIPO_VIVIENDA = [
        ('PRO', 'Propia'),
        ('PROHIP', 'Propia con hipoteca'),
        ('REN', 'Rentada'),
        ('PRE', 'Prestada'),
        ('FAM', 'Familiar'),
        ('OTR', 'Otro'),
    ]
    tipo_vivienda = models.CharField(max_length=6, choices=TIPO_VIVIENDA)

    # Características físicas
    material_construccion = models.CharField(max_length=100, blank=True)
    numero_habitaciones = models.IntegerField(validators=[MinValueValidator(1)])
    numero_niveles = models.IntegerField(default=1)

    # Servicios
    tiene_agua = models.BooleanField(default=False)
    tiene_luz = models.BooleanField(default=False)
    tiene_drenaje = models.BooleanField(default=False)
    tiene_gas = models.BooleanField(default=False)
    tiene_internet = models.BooleanField(default=False)
    tiene_tv_cable = models.BooleanField(default=False)

    # Tiempo de residencia
    tiempo_residencia_anios = models.IntegerField(validators=[MinValueValidator(0)])
    tiempo_residencia_meses = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(11)])

    class Meta:
        verbose_name_plural = "Domicilios"

    def __str__(self):
        return f"{self.calle} #{self.numero_exterior}, {self.colonia}"