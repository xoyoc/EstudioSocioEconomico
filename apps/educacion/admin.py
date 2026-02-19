from django.contrib import admin

from .models import NivelEducativo, Educacion


@admin.register(NivelEducativo)
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'orden', 'activo')
    list_editable = ('activo', 'orden')
    list_filter = ('activo',)
    search_fields = ('nivel',)


@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nivel', 'institucion', 'titulo',
                    'estado', 'anio_inicio', 'anio_fin',
                    'documento_verificado')
    list_filter = ('nivel', 'estado', 'documento_verificado')
    search_fields = ('persona__folio', 'persona__nombre',
                     'institucion', 'titulo')
    raw_id_fields = ('persona',)
    readonly_fields = ('created_at', 'updated_at',
                       'created_by', 'updated_by')
    list_per_page = 25

    fieldsets = (
        ('Persona', {
            'fields': ('persona',),
        }),
        ('Formación', {
            'fields': ('nivel', 'institucion', 'titulo', 'estado',
                       'anio_inicio', 'anio_fin'),
        }),
        ('Verificación', {
            'fields': ('tiene_cedula', 'numero_cedula',
                       'documento_verificado'),
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
