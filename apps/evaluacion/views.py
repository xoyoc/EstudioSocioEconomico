from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import EvaluacionRiesgo


class EvaluacionRiesgoListView(ListView):
    model = EvaluacionRiesgo
    context_object_name = 'evaluaciones'


class EvaluacionRiesgoDetailView(DetailView):
    model = EvaluacionRiesgo
    context_object_name = 'evaluacion'


class EvaluacionRiesgoCreateView(CreateView):
    model = EvaluacionRiesgo
    fields = [
        'estudio', 'evaluador',
        'puntuacion_identificacion', 'puntuacion_domicilio',
        'puntuacion_laboral', 'puntuacion_economica',
        'puntuacion_crediticia', 'puntuacion_referencias',
        'score_final', 'nivel_riesgo',
        'factores_riesgo', 'factores_atenuantes', 'recomendacion_final',
    ]
    success_url = reverse_lazy('evaluacion:evaluacionriesgo_list')


class EvaluacionRiesgoUpdateView(UpdateView):
    model = EvaluacionRiesgo
    fields = [
        'estudio', 'evaluador',
        'puntuacion_identificacion', 'puntuacion_domicilio',
        'puntuacion_laboral', 'puntuacion_economica',
        'puntuacion_crediticia', 'puntuacion_referencias',
        'score_final', 'nivel_riesgo',
        'factores_riesgo', 'factores_atenuantes', 'recomendacion_final',
    ]
    success_url = reverse_lazy('evaluacion:evaluacionriesgo_list')


class EvaluacionRiesgoDeleteView(DeleteView):
    model = EvaluacionRiesgo
    context_object_name = 'evaluacion'
    success_url = reverse_lazy('evaluacion:evaluacionriesgo_list')
