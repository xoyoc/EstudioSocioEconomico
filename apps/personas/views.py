from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Persona


class PersonaListView(ListView):
    model = Persona
    context_object_name = 'personas'


class PersonaDetailView(DetailView):
    model = Persona
    context_object_name = 'persona'


class PersonaCreateView(CreateView):
    model = Persona
    fields = [
        'nombre', 'apellido_paterno', 'apellido_materno',
        'fecha_nacimiento', 'tipo_identificacion', 'numero_identificacion',
        'curp', 'rfc', 'email', 'telefono_movil', 'telefono_fijo',
        'estado_civil', 'numero_dependientes', 'activo',
    ]
    success_url = reverse_lazy('personas:persona_list')


class PersonaUpdateView(UpdateView):
    model = Persona
    fields = [
        'nombre', 'apellido_paterno', 'apellido_materno',
        'fecha_nacimiento', 'tipo_identificacion', 'numero_identificacion',
        'curp', 'rfc', 'email', 'telefono_movil', 'telefono_fijo',
        'estado_civil', 'numero_dependientes', 'activo',
    ]
    success_url = reverse_lazy('personas:persona_list')


class PersonaDeleteView(DeleteView):
    model = Persona
    context_object_name = 'persona'
    success_url = reverse_lazy('personas:persona_list')
