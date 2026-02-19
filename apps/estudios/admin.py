from django.contrib import admin
from django.utils import timezone

from .models import EstudioSocioeconomico
from apps.economia.models import SituacionEconomica
from apps.evaluacion.models import EvaluacionRiesgo
from apps.visitas.models import VisitaDomiciliaria
from apps.documentos.models import Documento


class SituacionEconomicaInline(admin.StackedInline):
    model = SituacionEconomica
    extra = 0
    max_num = 1
    fieldsets = (
        ('Ingresos', {
            'fields': ('salario_mensual', 'bonos_comisiones', 'ingresos_extra',
                       'apoyo_familiar', 'otros_ingresos',
                       'descripcion_otros_ingresos'),
        }),
        ('Egresos', {
            'fields': ('gasto_alimentacion', 'gasto_vivienda',
                       'gasto_servicios', 'gasto_transporte',
                       'gasto_educacion', 'gasto_salud',
                       'gasto_deudas', 'otros_gastos',
                       'descripcion_otros_gastos'),
        }),
        ('Patrimonio', {
            'fields': ('tiene_automovil', 'automovil_marca_modelo',
                       'automovil_anio', 'patrimonio_inmobiliario',
                       'descripcion_patrimonio'),
        }),
        ('Créditos y deudas', {
            'fields': ('tiene_creditos', 'credito_hipotecario',
                       'credito_automotriz', 'tarjetas_credito',
                       'prestamos_personales', 'otros_creditos',
                       'descripcion_otros_creditos'),
        }),
    )


class EvaluacionRiesgoInline(admin.StackedInline):
    model = EvaluacionRiesgo
    extra = 0
    max_num = 1
    fieldsets = (
        ('Puntuaciones por categoría', {
            'fields': ('puntuacion_identificacion', 'puntuacion_domicilio',
                       'puntuacion_laboral', 'puntuacion_economica',
                       'puntuacion_crediticia', 'puntuacion_referencias'),
        }),
        ('Score y nivel de riesgo', {
            'fields': ('score_final', 'nivel_riesgo', 'evaluador'),
        }),
        ('Análisis', {
            'fields': ('factores_riesgo', 'factores_atenuantes',
                       'recomendacion_final'),
        }),
    )


class VisitaDomiciliariaInline(admin.StackedInline):
    model = VisitaDomiciliaria
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('evaluador', 'fecha_visita', 'latitud', 'longitud'),
        }),
        ('Resultados', {
            'fields': ('persona_encontrada', 'verificacion_domicilio'),
        }),
        ('Entorno', {
            'fields': ('tipo_zona', 'nivel_seguridad',
                       'nivel_ruido', 'acceso_transporte'),
        }),
        ('Comentarios', {
            'fields': ('observaciones_generales', 'recomendacion'),
            'classes': ('collapse',),
        }),
    )


class DocumentoEstudioInline(admin.TabularInline):
    model = Documento
    extra = 0
    fields = ('tipo', 'archivo', 'nombre_archivo', 'verificado',
              'verificado_por')
    readonly_fields = ('nombre_archivo',)


@admin.register(EstudioSocioeconomico)
class EstudioSocioeconomicoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_estudio', 'estado',
                    'fecha_programada_visita', 'puntuacion_total',
                    'created_at')
    list_filter = ('estado', 'tipo_estudio')
    search_fields = ('persona__folio', 'persona__nombre',
                     'persona__apellido_paterno')
    readonly_fields = ('puntuacion_total', 'created_at', 'updated_at',
                       'created_by', 'updated_by')
    date_hierarchy = 'created_at'
    list_per_page = 25
    raw_id_fields = ('persona',)

    fieldsets = (
        (None, {
            'fields': ('persona', 'tipo_estudio', 'estado'),
        }),
        ('Fechas', {
            'fields': ('fecha_programada_visita', 'fecha_realizacion',
                       'fecha_aprobacion'),
        }),
        ('Resultado', {
            'fields': ('puntuacion_total', 'observaciones', 'conclusion'),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    inlines = [SituacionEconomicaInline, EvaluacionRiesgoInline,
               VisitaDomiciliariaInline, DocumentoEstudioInline]

    actions = ['marcar_en_proceso', 'marcar_completado']

    @admin.action(description='Marcar como En proceso')
    def marcar_en_proceso(self, request, queryset):
        updated = queryset.filter(estado='BOR').update(estado='PRO')
        self.message_user(request, f'{updated} estudio(s) marcado(s) en proceso.')

    @admin.action(description='Marcar como Completado')
    def marcar_completado(self, request, queryset):
        updated = queryset.filter(estado='PRO').update(
            estado='COM', fecha_realizacion=timezone.now()
        )
        self.message_user(request, f'{updated} estudio(s) marcado(s) como completado(s).')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
