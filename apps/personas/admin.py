from django.contrib import admin

from .models import Persona
from apps.domicilios.models import Domicilio
from apps.educacion.models import Educacion
from apps.laboral.models import HistorialLaboral
from apps.familia.models import GrupoFamiliar
from apps.referencias.models import Referencia
from apps.documentos.models import Documento


class DomicilioInline(admin.StackedInline):
    model = Domicilio
    extra = 0
    fieldsets = (
        ('Tipo y dirección', {
            'fields': ('tipo', 'calle', 'numero_exterior', 'numero_interior',
                       'entre_calles', 'colonia', 'codigo_postal',
                       'municipio', 'estado', 'pais'),
        }),
        ('Vivienda', {
            'fields': ('tipo_vivienda', 'material_construccion',
                       'numero_habitaciones', 'numero_niveles'),
        }),
        ('Servicios', {
            'fields': ('tiene_agua', 'tiene_luz', 'tiene_drenaje',
                       'tiene_gas', 'tiene_internet', 'tiene_tv_cable'),
            'classes': ('collapse',),
        }),
        ('Tiempo de residencia', {
            'fields': ('tiempo_residencia_anios', 'tiempo_residencia_meses'),
        }),
    )


class EducacionInline(admin.TabularInline):
    model = Educacion
    extra = 0
    fields = ('nivel', 'institucion', 'titulo', 'estado',
              'anio_inicio', 'anio_fin', 'documento_verificado')


class HistorialLaboralInline(admin.TabularInline):
    model = HistorialLaboral
    extra = 0
    fields = ('empresa', 'puesto', 'fecha_inicio', 'fecha_fin',
              'es_trabajo_actual', 'salario_final', 'verificada')


class GrupoFamiliarInline(admin.TabularInline):
    model = GrupoFamiliar
    extra = 0
    fields = ('nombre_completo', 'parentesco', 'edad',
              'tipo_dependencia', 'vive_en_domicilio',
              'aporta_ingreso', 'monto_aportacion')


class ReferenciaInline(admin.TabularInline):
    model = Referencia
    extra = 0
    fields = ('tipo', 'nombre', 'telefono',
              'parentesco_o_relacion', 'tiempo_conocer_anios', 'verificada')


class DocumentoPersonaInline(admin.TabularInline):
    model = Documento
    extra = 0
    fields = ('tipo', 'archivo', 'nombre_archivo', 'verificado')
    readonly_fields = ('nombre_archivo',)


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('folio', 'get_nombre_completo', 'curp',
                    'telefono_movil', 'estado_civil', 'activo')
    list_filter = ('activo', 'estado_civil', 'tipo_identificacion')
    search_fields = ('folio', 'nombre', 'apellido_paterno',
                     'apellido_materno', 'curp', 'email')
    readonly_fields = ('folio', 'created_at', 'updated_at',
                       'created_by', 'updated_by')
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información básica', {
            'fields': ('folio', 'nombre', 'apellido_paterno',
                       'apellido_materno', 'fecha_nacimiento'),
        }),
        ('Identificación oficial', {
            'fields': ('tipo_identificacion', 'numero_identificacion',
                       'curp', 'rfc'),
        }),
        ('Contacto', {
            'fields': ('email', 'telefono_movil', 'telefono_fijo'),
        }),
        ('Estado civil y familia', {
            'fields': ('estado_civil', 'numero_dependientes'),
        }),
        ('Control', {
            'fields': ('activo',),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    inlines = [DomicilioInline, EducacionInline, HistorialLaboralInline,
               GrupoFamiliarInline, ReferenciaInline, DocumentoPersonaInline]

    @admin.display(description='Nombre completo')
    def get_nombre_completo(self, obj):
        return obj.nombre_completo

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
