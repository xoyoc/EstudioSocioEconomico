from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import VisitaDomiciliaria


class VisitaDomiciliariaListView(ListView):
    model = VisitaDomiciliaria
    context_object_name = 'visitas'


class VisitaDomiciliariaDetailView(DetailView):
    model = VisitaDomiciliaria
    context_object_name = 'visita'


class VisitaDomiciliariaCreateView(CreateView):
    model = VisitaDomiciliaria
    fields = [
        'estudio', 'evaluador', 'fecha_visita',
        'latitud', 'longitud',
        'persona_encontrada', 'verificacion_domicilio',
        'tipo_zona', 'nivel_seguridad', 'nivel_ruido', 'acceso_transporte',
        'observaciones_generales', 'recomendacion',
    ]
    success_url = reverse_lazy('visitas:visitadomiciliaria_list')


class VisitaDomiciliariaUpdateView(UpdateView):
    model = VisitaDomiciliaria
    fields = [
        'estudio', 'evaluador', 'fecha_visita',
        'latitud', 'longitud',
        'persona_encontrada', 'verificacion_domicilio',
        'tipo_zona', 'nivel_seguridad', 'nivel_ruido', 'acceso_transporte',
        'observaciones_generales', 'recomendacion',
    ]
    success_url = reverse_lazy('visitas:visitadomiciliaria_list')


class VisitaDomiciliariaDeleteView(DeleteView):
    model = VisitaDomiciliaria
    context_object_name = 'visita'
    success_url = reverse_lazy('visitas:visitadomiciliaria_list')
