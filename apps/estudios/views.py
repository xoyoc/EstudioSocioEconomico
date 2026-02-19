from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import EstudioSocioeconomico


class EstudioListView(ListView):
    model = EstudioSocioeconomico
    context_object_name = 'estudios'


class EstudioDetailView(DetailView):
    model = EstudioSocioeconomico
    context_object_name = 'estudio'


class EstudioCreateView(CreateView):
    model = EstudioSocioeconomico
    fields = [
        'persona', 'tipo_estudio', 'estado',
        'fecha_programada_visita', 'fecha_realizacion', 'fecha_aprobacion',
        'observaciones', 'conclusion', 'puntuacion_total',
    ]
    success_url = reverse_lazy('estudios:estudio_list')


class EstudioUpdateView(UpdateView):
    model = EstudioSocioeconomico
    fields = [
        'persona', 'tipo_estudio', 'estado',
        'fecha_programada_visita', 'fecha_realizacion', 'fecha_aprobacion',
        'observaciones', 'conclusion', 'puntuacion_total',
    ]
    success_url = reverse_lazy('estudios:estudio_list')


class EstudioDeleteView(DeleteView):
    model = EstudioSocioeconomico
    context_object_name = 'estudio'
    success_url = reverse_lazy('estudios:estudio_list')
