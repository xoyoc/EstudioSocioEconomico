from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Domicilio


class DomicilioListView(ListView):
    model = Domicilio
    context_object_name = 'domicilios'


class DomicilioDetailView(DetailView):
    model = Domicilio
    context_object_name = 'domicilio'


class DomicilioCreateView(CreateView):
    model = Domicilio
    fields = [
        'persona', 'tipo',
        'calle', 'numero_exterior', 'numero_interior', 'entre_calles',
        'colonia', 'codigo_postal', 'municipio', 'estado', 'pais',
        'tipo_vivienda', 'material_construccion',
        'numero_habitaciones', 'numero_niveles',
        'tiene_agua', 'tiene_luz', 'tiene_drenaje',
        'tiene_gas', 'tiene_internet', 'tiene_tv_cable',
        'tiempo_residencia_anios', 'tiempo_residencia_meses',
    ]
    success_url = reverse_lazy('domicilios:domicilio_list')


class DomicilioUpdateView(UpdateView):
    model = Domicilio
    fields = [
        'persona', 'tipo',
        'calle', 'numero_exterior', 'numero_interior', 'entre_calles',
        'colonia', 'codigo_postal', 'municipio', 'estado', 'pais',
        'tipo_vivienda', 'material_construccion',
        'numero_habitaciones', 'numero_niveles',
        'tiene_agua', 'tiene_luz', 'tiene_drenaje',
        'tiene_gas', 'tiene_internet', 'tiene_tv_cable',
        'tiempo_residencia_anios', 'tiempo_residencia_meses',
    ]
    success_url = reverse_lazy('domicilios:domicilio_list')


class DomicilioDeleteView(DeleteView):
    model = Domicilio
    context_object_name = 'domicilio'
    success_url = reverse_lazy('domicilios:domicilio_list')
