from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import HistorialLaboral


class HistorialLaboralListView(ListView):
    model = HistorialLaboral
    context_object_name = 'historiales_laborales'


class HistorialLaboralDetailView(DetailView):
    model = HistorialLaboral
    context_object_name = 'historial_laboral'


class HistorialLaboralCreateView(CreateView):
    model = HistorialLaboral
    fields = [
        'persona', 'empresa', 'puesto', 'telefono_empresa',
        'fecha_inicio', 'fecha_fin', 'es_trabajo_actual',
        'salario_inicial', 'salario_final',
        'nombre_jefe', 'telefono_jefe', 'motivo_separacion',
        'verificada', 'fecha_verificacion',
    ]
    success_url = reverse_lazy('laboral:historiallaboral_list')


class HistorialLaboralUpdateView(UpdateView):
    model = HistorialLaboral
    fields = [
        'persona', 'empresa', 'puesto', 'telefono_empresa',
        'fecha_inicio', 'fecha_fin', 'es_trabajo_actual',
        'salario_inicial', 'salario_final',
        'nombre_jefe', 'telefono_jefe', 'motivo_separacion',
        'verificada', 'fecha_verificacion',
    ]
    success_url = reverse_lazy('laboral:historiallaboral_list')


class HistorialLaboralDeleteView(DeleteView):
    model = HistorialLaboral
    context_object_name = 'historial_laboral'
    success_url = reverse_lazy('laboral:historiallaboral_list')
