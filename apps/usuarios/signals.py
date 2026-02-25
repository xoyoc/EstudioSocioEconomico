"""
Crea automáticamente un PerfilUsuario cuando se crea un nuevo auth.User.
Si el usuario es superusuario (is_superuser=True) se le asigna rol ANA por defecto.
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(
            usuario=instance,
            defaults={'rol': 'ANA'},
        )
