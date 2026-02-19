from django.contrib import admin

from .models import EvaluacionRiesgo


@admin.register(EvaluacionRiesgo)
class EvaluacionRiesgoAdmin(admin.ModelAdmin):
    list_display = ('estudio', 'score_final', 'nivel_riesgo', 'evaluador')
    list_filter = ('nivel_riesgo',)
    search_fields = ('estudio__persona__folio',
                     'estudio__persona__nombre',
                     'evaluador__username')
    raw_id_fields = ('estudio',)
    list_per_page = 25

    fieldsets = (
        ('Estudio', {
            'fields': ('estudio', 'evaluador'),
        }),
        ('Puntuaciones por categoría', {
            'fields': ('puntuacion_identificacion', 'puntuacion_domicilio',
                       'puntuacion_laboral', 'puntuacion_economica',
                       'puntuacion_crediticia', 'puntuacion_referencias'),
        }),
        ('Score y nivel de riesgo', {
            'fields': ('score_final', 'nivel_riesgo'),
        }),
        ('Análisis', {
            'fields': ('factores_riesgo', 'factores_atenuantes',
                       'recomendacion_final'),
        }),
    )
