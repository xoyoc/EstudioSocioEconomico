from django.contrib import admin

from .models import TipoEstudio


@admin.register(TipoEstudio)
class TipoEstudioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'requiere_visita',
                    'requiere_verificacion_laboral',
                    'puntuacion_minima_aprobacion', 'orden')
    list_filter = ('activo', 'requiere_visita', 'requiere_verificacion_laboral')
    list_editable = ('activo', 'orden')
    search_fields = ('nombre', 'descripcion')
    ordering = ('orden', 'nombre')
