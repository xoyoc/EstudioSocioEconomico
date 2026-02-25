from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from .forms import PerfilUsuarioForm
from .mixins import AnalistaRequeridoMixin
from .models import PerfilUsuario


class MiPerfilView(LoginRequiredMixin, DetailView):
    """Muestra el perfil del usuario autenticado."""
    template_name = 'usuarios/mi_perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=self.request.user,
            defaults={'rol': 'ANA'},
        )
        return perfil


class MiPerfilEditarView(LoginRequiredMixin, UpdateView):
    """Permite al usuario editar su propio perfil (rol y teléfono)."""
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil_form.html'
    success_url = reverse_lazy('usuarios:mi_perfil')

    def get_object(self, queryset=None):
        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=self.request.user,
            defaults={'rol': 'ANA'},
        )
        return perfil

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['es_edicion_rol'] = False
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)


class UsuarioListView(AnalistaRequeridoMixin, ListView):
    """Lista de usuarios y sus roles — solo accesible para analistas."""
    model = PerfilUsuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'perfiles'
    paginate_by = 25

    def get_queryset(self):
        return PerfilUsuario.objects.select_related('usuario').order_by(
            'usuario__last_name', 'usuario__first_name'
        )


class UsuarioRolEditarView(AnalistaRequeridoMixin, UpdateView):
    """Permite a analistas cambiar el rol de otro usuario."""
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil_form.html'
    success_url = reverse_lazy('usuarios:usuario_list')

    def get_object(self, queryset=None):
        usuario = get_object_or_404(User, pk=self.kwargs['user_pk'])
        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=usuario,
            defaults={'rol': 'ANA'},
        )
        return perfil

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['es_edicion_rol'] = True
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Rol del usuario actualizado.')
        return super().form_valid(form)
