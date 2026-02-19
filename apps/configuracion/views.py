from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import TipoEstudio


class TipoEstudioListView(ListView):
    model = TipoEstudio
    context_object_name = 'tipos_estudio'


class TipoEstudioDetailView(DetailView):
    model = TipoEstudio
    context_object_name = 'tipo_estudio'


class TipoEstudioCreateView(CreateView):
    model = TipoEstudio
    fields = [
        'nombre', 'descripcion', 'activo', 'orden',
        'requiere_visita', 'requiere_verificacion_laboral',
        'puntuacion_minima_aprobacion',
    ]
    success_url = reverse_lazy('configuracion:tipoestudio_list')


class TipoEstudioUpdateView(UpdateView):
    model = TipoEstudio
    fields = [
        'nombre', 'descripcion', 'activo', 'orden',
        'requiere_visita', 'requiere_verificacion_laboral',
        'puntuacion_minima_aprobacion',
    ]
    success_url = reverse_lazy('configuracion:tipoestudio_list')


class TipoEstudioDeleteView(DeleteView):
    model = TipoEstudio
    context_object_name = 'tipo_estudio'
    success_url = reverse_lazy('configuracion:tipoestudio_list')
