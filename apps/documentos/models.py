from django.contrib.auth.models import User
from django.db import models

from apps.configuracion.models import TimestampModel
from apps.estudios.models import EstudioSocioeconomico
from apps.personas.models import Persona

class Documento(TimestampModel):
    """Modelo para almacenar documentos digitalizados"""
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='documentos')
    estudio = models.ForeignKey(EstudioSocioeconomico, on_delete=models.CASCADE, related_name='documentos', null=True, blank=True)

    TIPO_DOCUMENTO = [
        ('IDE', 'Identificación oficial'),
        ('DOM', 'Comprobante de domicilio'),
        ('ING', 'Comprobante de ingresos'),
        ('EST', 'Estado de cuenta'),
        ('TIT', 'Título/Cédula'),
        ('ACT', 'Acta de nacimiento'),
        ('CUR', 'CURP'),
        ('RFC', 'RFC'),
        ('FOT', 'Fotografía'),
        ('OTR', 'Otro'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPO_DOCUMENTO)

    archivo = models.FileField(upload_to='documentos/%Y/%m/%d/')
    nombre_archivo = models.CharField(max_length=255)
    tamaño = models.IntegerField(help_text="Tamaño en bytes")

    verificado = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    verificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_verificados')

    class Meta:
        verbose_name_plural = "Documentos"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.persona.nombre_completo}"
