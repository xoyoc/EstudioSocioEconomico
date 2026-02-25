from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil y rol'
    fields = ('rol', 'telefono', 'activo')
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [PerfilUsuarioInline]


# Re-registrar User con el nuevo admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'telefono', 'activo', 'created_at')
    list_filter = ('rol', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
    list_editable = ('rol', 'activo')
