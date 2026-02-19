from django.contrib import admin
from django.utils import timezone

from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'prioridad',
                    'leida', 'fecha_lectura', 'created_at')
    list_filter = ('tipo', 'prioridad', 'leida')
    search_fields = ('titulo', 'mensaje', 'usuario__username')
    raw_id_fields = ('estudio',)
    readonly_fields = ('fecha_lectura', 'created_at', 'updated_at',
                       'created_by', 'updated_by')
    date_hierarchy = 'created_at'
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('usuario', 'estudio', 'tipo', 'prioridad'),
        }),
        ('Contenido', {
            'fields': ('titulo', 'mensaje'),
        }),
        ('Estado', {
            'fields': ('leida', 'fecha_lectura'),
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at',
                       'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    actions = ['marcar_leidas']

    @admin.action(description='Marcar como leídas')
    def marcar_leidas(self, request, queryset):
        updated = queryset.filter(leida=False).update(
            leida=True, fecha_lectura=timezone.now()
        )
        self.message_user(request, f'{updated} notificación(es) marcada(s) como leída(s).')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
