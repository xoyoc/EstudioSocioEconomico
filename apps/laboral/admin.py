from django.contrib import admin
from django.utils import timezone

from .models import HistorialLaboral


@admin.register(HistorialLaboral)
class HistorialLaboralAdmin(admin.ModelAdmin):
    list_display = ('persona', 'empresa', 'puesto',
                    'fecha_inicio', 'fecha_fin',
                    'es_trabajo_actual', 'verificada',
                    'fecha_verificacion')
    list_filter = ('es_trabajo_actual', 'verificada')
    search_fields = ('persona__folio', 'persona__nombre',
                     'empresa', 'puesto')
    raw_id_fields = ('persona',)
    readonly_fields = ('fecha_verificacion', 'created_at',
                       'updated_at', 'created_by', 'updated_by')
    list_per_page = 25

    fieldsets = (
        ('Persona', {
            'fields': ('persona',),
        }),
        ('Empresa', {
            'fields': ('empresa', 'puesto', 'telefono_empresa'),
        }),
        ('Periodo', {
            'fields': ('fecha_inicio', 'fecha_fin', 'es_trabajo_actual'),
        }),
        ('Salario', {
            'fields': ('salario_inicial', 'salario_final'),
        }),
        ('Jefe directo', {
            'fields': ('nombre_jefe', 'telefono_jefe'),
        }),
        ('Separación y verificación', {
            'fields': ('motivo_separacion', 'verificada',
                       'fecha_verificacion'),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    actions = ['marcar_verificada']

    @admin.action(description='Marcar como verificada')
    def marcar_verificada(self, request, queryset):
        updated = queryset.filter(verificada=False).update(
            verificada=True, fecha_verificacion=timezone.now()
        )
        self.message_user(request, f'{updated} registro(s) marcado(s) como verificado(s).')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
