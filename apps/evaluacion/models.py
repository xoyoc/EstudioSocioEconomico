from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.estudios.models import EstudioSocioeconomico

class EvaluacionRiesgo(models.Model):
    """Modelo para evaluación de riesgos y scoring"""
    estudio = models.OneToOneField(EstudioSocioeconomico, on_delete=models.CASCADE, related_name='evaluacion_riesgo')
    evaluador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Puntuaciones por categoría (0-100)
    puntuacion_identificacion = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    puntuacion_domicilio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    puntuacion_laboral = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    puntuacion_economica = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    puntuacion_crediticia = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    puntuacion_referencias = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Score total
    score_final = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    NIVEL_RIESGO = [
        ('BAJ', 'Bajo'),
        ('MED', 'Medio'),
        ('ALT', 'Alto'),
        ('CRI', 'Crítico'),
    ]
    nivel_riesgo = models.CharField(max_length=3, choices=NIVEL_RIESGO)

    factores_riesgo = models.TextField(blank=True)
    factores_atenuantes = models.TextField(blank=True)

    recomendacion_final = models.TextField()

    class Meta:
        verbose_name_plural = "Evaluaciones de riesgo"

    def __str__(self):
        return f"Evaluación {self.estudio.persona.folio} - Score: {self.score_final}"
