from django.core.validators import MinValueValidator
from django.db import models

from apps.estudios.models import EstudioSocioeconomico

class SituacionEconomica(models.Model):
    """Modelo de situación económica - Uno por estudio"""
    estudio = models.OneToOneField(EstudioSocioeconomico, on_delete=models.CASCADE, related_name='situacion_economica')

    # Ingresos
    salario_mensual = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bonos_comisiones = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    ingresos_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    apoyo_familiar = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    descripcion_otros_ingresos = models.CharField(max_length=200, blank=True)

    # Egresos
    gasto_alimentacion = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_vivienda = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_servicios = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_transporte = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_educacion = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_salud = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gasto_deudas = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_gastos = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    descripcion_otros_gastos = models.CharField(max_length=200, blank=True)

    # Patrimonio
    tiene_automovil = models.BooleanField(default=False)
    automovil_marca_modelo = models.CharField(max_length=100, blank=True)
    automovil_anio = models.IntegerField(null=True, blank=True)

    TIPO_VIVIENDA_PATRIMONIO = [
        ('NINGUNA', 'Sin vivienda'),
        ('PROPIA', 'Vivienda propia'),
        ('INVERSION', 'Vivienda en inversión'),
        ('TERRENO', 'Terreno'),
        ('OTRO', 'Otro'),
    ]
    patrimonio_inmobiliario = models.CharField(max_length=20, choices=TIPO_VIVIENDA_PATRIMONIO, default='NINGUNA')
    descripcion_patrimonio = models.TextField(blank=True)

    # Créditos y deudas
    tiene_creditos = models.BooleanField(default=False)
    credito_hipotecario = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    credito_automotriz = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tarjetas_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    prestamos_personales = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_creditos = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    descripcion_otros_creditos = models.CharField(max_length=200, blank=True)

    @property
    def ingreso_total_mensual(self):
        return (self.salario_mensual + self.bonos_comisiones +
                self.ingresos_extra + self.apoyo_familiar + self.otros_ingresos)

    @property
    def egreso_total_mensual(self):
        return (self.gasto_alimentacion + self.gasto_vivienda + self.gasto_servicios +
                self.gasto_transporte + self.gasto_educacion + self.gasto_salud +
                self.gasto_deudas + self.otros_gastos)

    @property
    def capacidad_ahorro(self):
        return self.ingreso_total_mensual - self.egreso_total_mensual

    class Meta:
        verbose_name_plural = "Situaciones económicas"