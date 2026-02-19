from django.contrib import admin

from .models import Domicilio


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo', 'calle', 'colonia',
                    'municipio', 'estado', 'tipo_vivienda')
    list_filter = ('tipo', 'tipo_vivienda', 'estado')
    search_fields = ('persona__folio', 'persona__nombre',
                     'calle', 'colonia', 'codigo_postal')
    raw_id_fields = ('persona',)
    readonly_fields = ('created_at', 'updated_at',
                       'created_by', 'updated_by')
    list_per_page = 25

    fieldsets = (
        ('Persona', {
            'fields': ('persona', 'tipo'),
        }),
        ('Dirección', {
            'fields': ('calle', 'numero_exterior', 'numero_interior',
                       'entre_calles', 'colonia', 'codigo_postal',
                       'municipio', 'estado', 'pais'),
        }),
        ('Características de la vivienda', {
            'fields': ('tipo_vivienda', 'material_construccion',
                       'numero_habitaciones', 'numero_niveles'),
        }),
        ('Servicios', {
            'fields': ('tiene_agua', 'tiene_luz', 'tiene_drenaje',
                       'tiene_gas', 'tiene_internet', 'tiene_tv_cable'),
        }),
        ('Tiempo de residencia', {
            'fields': ('tiempo_residencia_anios', 'tiempo_residencia_meses'),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
