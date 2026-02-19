from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

from apps.configuracion.models import TimestampModel


class Persona(TimestampModel):
    """Modelo principal de la persona evaluada"""
    # Información básica
    folio = models.CharField(max_length=20, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField()

    # Identificación oficial
    TIPO_IDENTIFICACION = [
        ('INE', 'INE/IFE'),
        ('PAS', 'Pasaporte'),
        ('CED', 'Cédula Profesional'),
        ('CAR', 'Cartilla Militar'),
        ('OTR', 'Otro'),
    ]
    tipo_identificacion = models.CharField(max_length=3, choices=TIPO_IDENTIFICACION)
    numero_identificacion = models.CharField(max_length=50)
    curp = models.CharField(max_length=18, validators=[RegexValidator(r'^[A-Z0-9]{18}$', 'CURP inválida')])
    rfc = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r'^[A-Z&Ñ]{4}\d{6}[A-Z0-9]{3}$', 'RFC inválido')])

    # Contacto
    email = models.EmailField()
    telefono_movil = models.CharField(max_length=15)
    telefono_fijo = models.CharField(max_length=15, blank=True)

    # Estado civil y familia
    ESTADO_CIVIL = [
        ('SOL', 'Soltero/a'),
        ('CAS', 'Casado/a'),
        ('ULB', 'Unión Libre'),
        ('DIV', 'Divorciado/a'),
        ('VIU', 'Viudo/a'),
        ('SEP', 'Separado/a'),
    ]
    estado_civil = models.CharField(max_length=3, choices=ESTADO_CIVIL)
    numero_dependientes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Campos de auditoría
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Personas"
        indexes = [
            models.Index(fields=['folio']),
            models.Index(fields=['curp']),
            models.Index(fields=['apellido_paterno', 'apellido_materno', 'nombre']),
        ]

    def save(self, *args, **kwargs):
        if not self.folio:
            # Generar folio único: AÑO-MES-SECUENCIA
            year = timezone.now().strftime('%Y')
            month = timezone.now().strftime('%m')
            last_study = Persona.objects.filter(
                folio__startswith=f'{year}{month}'
            ).order_by('-folio').first()

            if last_study:
                last_sequence = int(last_study.folio[-4:])
                new_sequence = str(last_sequence + 1).zfill(4)
            else:
                new_sequence = '0001'

            self.folio = f'{year}{month}{new_sequence}'

        super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return f"{self.folio} - {self.nombre_completo}"