from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Referencia


class ReferenciaListView(ListView):
    model = Referencia
    context_object_name = 'referencias'


class ReferenciaDetailView(DetailView):
    model = Referencia
    context_object_name = 'referencia'


class ReferenciaCreateView(CreateView):
    model = Referencia
    fields = [
        'persona', 'tipo', 'nombre', 'telefono', 'email',
        'parentesco_o_relacion', 'tiempo_conocer_anios', 'domicilio',
        'verificada', 'fecha_verificacion', 'comentarios_verificacion',
    ]
    success_url = reverse_lazy('referencias:referencia_list')


class ReferenciaUpdateView(UpdateView):
    model = Referencia
    fields = [
        'persona', 'tipo', 'nombre', 'telefono', 'email',
        'parentesco_o_relacion', 'tiempo_conocer_anios', 'domicilio',
        'verificada', 'fecha_verificacion', 'comentarios_verificacion',
    ]
    success_url = reverse_lazy('referencias:referencia_list')


class ReferenciaDeleteView(DeleteView):
    model = Referencia
    context_object_name = 'referencia'
    success_url = reverse_lazy('referencias:referencia_list')
