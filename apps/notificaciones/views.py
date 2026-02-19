from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Notificacion


class NotificacionListView(ListView):
    model = Notificacion
    context_object_name = 'notificaciones'


class NotificacionDetailView(DetailView):
    model = Notificacion
    context_object_name = 'notificacion'


class NotificacionCreateView(CreateView):
    model = Notificacion
    fields = [
        'usuario', 'estudio', 'tipo',
        'titulo', 'mensaje', 'prioridad',
        'leida', 'fecha_lectura',
    ]
    success_url = reverse_lazy('notificaciones:notificacion_list')


class NotificacionUpdateView(UpdateView):
    model = Notificacion
    fields = [
        'usuario', 'estudio', 'tipo',
        'titulo', 'mensaje', 'prioridad',
        'leida', 'fecha_lectura',
    ]
    success_url = reverse_lazy('notificaciones:notificacion_list')


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    context_object_name = 'notificacion'
    success_url = reverse_lazy('notificaciones:notificacion_list')
