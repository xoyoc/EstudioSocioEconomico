from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Documento


class DocumentoListView(ListView):
    model = Documento
    context_object_name = 'documentos'


class DocumentoDetailView(DetailView):
    model = Documento
    context_object_name = 'documento'


class DocumentoCreateView(CreateView):
    model = Documento
    fields = [
        'persona', 'estudio', 'tipo',
        'archivo', 'nombre_archivo', 'tamaño',
        'verificado', 'fecha_verificacion', 'verificado_por',
    ]
    success_url = reverse_lazy('documentos:documento_list')


class DocumentoUpdateView(UpdateView):
    model = Documento
    fields = [
        'persona', 'estudio', 'tipo',
        'archivo', 'nombre_archivo', 'tamaño',
        'verificado', 'fecha_verificacion', 'verificado_por',
    ]
    success_url = reverse_lazy('documentos:documento_list')


class DocumentoDeleteView(DeleteView):
    model = Documento
    context_object_name = 'documento'
    success_url = reverse_lazy('documentos:documento_list')
