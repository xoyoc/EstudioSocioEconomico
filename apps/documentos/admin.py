from django.contrib import admin
from django.utils import timezone

from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo', 'nombre_archivo',
                    'verificado', 'fecha_verificacion',
                    'verificado_por')
    list_filter = ('tipo', 'verificado')
    search_fields = ('persona__folio', 'persona__nombre',
                     'nombre_archivo')
    raw_id_fields = ('persona', 'estudio')
    readonly_fields = ('fecha_verificacion', 'verificado_por',
                       'created_at', 'updated_at',
                       'created_by', 'updated_by')
    list_per_page = 25

    fieldsets = (
        ('Asociación', {
            'fields': ('persona', 'estudio'),
        }),
        ('Documento', {
            'fields': ('tipo', 'archivo', 'nombre_archivo', 'tamaño'),
        }),
        ('Verificación', {
            'fields': ('verificado', 'fecha_verificacion',
                       'verificado_por'),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    actions = ['marcar_verificado']

    @admin.action(description='Marcar como verificado')
    def marcar_verificado(self, request, queryset):
        updated = queryset.filter(verificado=False).update(
            verificado=True,
            fecha_verificacion=timezone.now(),
            verificado_por=request.user,
        )
        self.message_user(request, f'{updated} documento(s) marcado(s) como verificado(s).')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
