from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import GrupoFamiliar


class GrupoFamiliarListView(ListView):
    model = GrupoFamiliar
    context_object_name = 'grupos_familiares'


class GrupoFamiliarDetailView(DetailView):
    model = GrupoFamiliar
    context_object_name = 'grupo_familiar'


class GrupoFamiliarCreateView(CreateView):
    model = GrupoFamiliar
    fields = [
        'persona', 'nombre_completo', 'parentesco', 'edad',
        'tipo_dependencia', 'ocupacion', 'escolaridad',
        'vive_en_domicilio', 'aporta_ingreso', 'monto_aportacion',
    ]
    success_url = reverse_lazy('familia:grupofamiliar_list')


class GrupoFamiliarUpdateView(UpdateView):
    model = GrupoFamiliar
    fields = [
        'persona', 'nombre_completo', 'parentesco', 'edad',
        'tipo_dependencia', 'ocupacion', 'escolaridad',
        'vive_en_domicilio', 'aporta_ingreso', 'monto_aportacion',
    ]
    success_url = reverse_lazy('familia:grupofamiliar_list')


class GrupoFamiliarDeleteView(DeleteView):
    model = GrupoFamiliar
    context_object_name = 'grupo_familiar'
    success_url = reverse_lazy('familia:grupofamiliar_list')
