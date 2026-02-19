from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import NivelEducativo, Educacion


# --- NivelEducativo ---

class NivelEducativoListView(ListView):
    model = NivelEducativo
    context_object_name = 'niveles_educativos'


class NivelEducativoDetailView(DetailView):
    model = NivelEducativo
    context_object_name = 'nivel_educativo'


class NivelEducativoCreateView(CreateView):
    model = NivelEducativo
    fields = ['nivel', 'orden', 'activo']
    success_url = reverse_lazy('educacion:niveleducativo_list')


class NivelEducativoUpdateView(UpdateView):
    model = NivelEducativo
    fields = ['nivel', 'orden', 'activo']
    success_url = reverse_lazy('educacion:niveleducativo_list')


class NivelEducativoDeleteView(DeleteView):
    model = NivelEducativo
    context_object_name = 'nivel_educativo'
    success_url = reverse_lazy('educacion:niveleducativo_list')


# --- Educacion ---

class EducacionListView(ListView):
    model = Educacion
    context_object_name = 'educaciones'


class EducacionDetailView(DetailView):
    model = Educacion
    context_object_name = 'educacion'


class EducacionCreateView(CreateView):
    model = Educacion
    fields = [
        'persona', 'nivel', 'institucion', 'titulo', 'estado',
        'anio_inicio', 'anio_fin',
        'tiene_cedula', 'numero_cedula', 'documento_verificado',
    ]
    success_url = reverse_lazy('educacion:educacion_list')


class EducacionUpdateView(UpdateView):
    model = Educacion
    fields = [
        'persona', 'nivel', 'institucion', 'titulo', 'estado',
        'anio_inicio', 'anio_fin',
        'tiene_cedula', 'numero_cedula', 'documento_verificado',
    ]
    success_url = reverse_lazy('educacion:educacion_list')


class EducacionDeleteView(DeleteView):
    model = Educacion
    context_object_name = 'educacion'
    success_url = reverse_lazy('educacion:educacion_list')
