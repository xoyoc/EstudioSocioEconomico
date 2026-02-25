from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Notificacion


class NotificacionListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'notificaciones/notificacion_list.html'
    context_object_name = 'notificaciones'
    paginate_by = 25

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['no_leidas'] = self.get_queryset().filter(leida=False).count()
        return ctx


class NotificacionDetailView(LoginRequiredMixin, DetailView):
    model = Notificacion
    template_name = 'notificaciones/notificacion_detail.html'
    context_object_name = 'notificacion'

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        notif = self.get_object()
        if not notif.leida:
            notif.leida = True
            notif.fecha_lectura = timezone.now()
            notif.save(update_fields=['leida', 'fecha_lectura'])
        return response


class NotificacionCreateView(LoginRequiredMixin, CreateView):
    model = Notificacion
    template_name = 'notificaciones/notificacion_form.html'
    fields = [
        'usuario', 'estudio', 'tipo',
        'titulo', 'mensaje', 'prioridad',
    ]
    success_url = '/notificaciones/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class NotificacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Notificacion
    template_name = 'notificaciones/notificacion_form.html'
    fields = [
        'usuario', 'estudio', 'tipo',
        'titulo', 'mensaje', 'prioridad',
        'leida', 'fecha_lectura',
    ]
    success_url = '/notificaciones/'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class NotificacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Notificacion
    template_name = 'notificaciones/notificacion_confirm_delete.html'
    context_object_name = 'notificacion'
    success_url = '/notificaciones/'


class MarcarLeidaView(LoginRequiredMixin, View):
    """Marca una notificación del usuario autenticado como leída (vía POST o HTMX)."""

    def post(self, request, pk):
        notif = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
        if not notif.leida:
            notif.leida = True
            notif.fecha_lectura = timezone.now()
            notif.save(update_fields=['leida', 'fecha_lectura'])
        # Si es HTMX retorna fragmento vacío; si no, redirige
        if request.headers.get('HX-Request'):
            return HttpResponse(status=204)
        next_url = request.POST.get('next') or '/notificaciones/'
        return redirect(next_url)


class MarcarTodasLeidasView(LoginRequiredMixin, View):
    """Marca todas las notificaciones no leídas del usuario como leídas."""

    def post(self, request):
        Notificacion.objects.filter(
            usuario=request.user, leida=False
        ).update(leida=True, fecha_lectura=timezone.now())
        if request.headers.get('HX-Request'):
            return HttpResponse(status=204)
        return redirect('/notificaciones/')


class NotifCountView(LoginRequiredMixin, View):
    """
    Devuelve el componente notif_badge.html con el conteo actual de
    notificaciones no leídas — usado por el HTMX polling del navbar.
    """

    def get(self, request):
        count = Notificacion.objects.filter(
            usuario=request.user, leida=False
        ).count()
        from django.template.loader import render_to_string
        html = render_to_string(
            'components/notif_badge.html',
            {'notif_count': count},
            request=request,
        )
        return HttpResponse(html)
