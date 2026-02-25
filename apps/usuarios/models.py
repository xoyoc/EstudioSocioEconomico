from django.contrib.auth.models import User
from django.db import models


class PerfilUsuario(models.Model):
    """
    Extiende auth.User con el rol operativo dentro del sistema.

    Roles:
      ANA — Analista / Colaborador interno: acceso total a todos los módulos.
      INS — Inspector / Personal de campo: acceso limitado a visitas, agenda
            y verificación de referencias/laboral.
    """
    ROL_CHOICES = [
        ('ANA', 'Analista'),
        ('INS', 'Inspector'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario',
    )
    rol = models.CharField(
        max_length=3,
        choices=ROL_CHOICES,
        default='ANA',
        verbose_name='Rol',
        help_text='Determina las funciones a las que tiene acceso el usuario.',
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono',
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Desactiva para suspender el acceso sin borrar el usuario.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'
        ordering = ['usuario__last_name', 'usuario__first_name']

    def __str__(self):
        nombre = self.usuario.get_full_name() or self.usuario.username
        return f'{nombre} ({self.get_rol_display()})'

    @property
    def es_analista(self):
        return self.rol == 'ANA'

    @property
    def es_inspector(self):
        return self.rol == 'INS'
