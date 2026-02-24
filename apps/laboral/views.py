from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .forms import HistorialLaboralForm
from .models import HistorialLaboral


class HistorialLaboralListView(LoginRequiredMixin, ListView):
    model = HistorialLaboral
    context_object_name = 'historiales_laborales'
    paginate_by = 25


class HistorialLaboralDetailView(LoginRequiredMixin, DetailView):
    model = HistorialLaboral
    context_object_name = 'historial_laboral'


class HistorialLaboralCreateView(LoginRequiredMixin, CreateView):
    model = HistorialLaboral
    form_class = HistorialLaboralForm
    success_url = reverse_lazy('laboral:historiallaboral_list')

    def get_initial(self):
        initial = super().get_initial()
        persona_pk = self.request.GET.get('persona')
        if persona_pk:
            initial['persona'] = persona_pk
        return initial

    def get_success_url(self):
        back = self.request.GET.get('back')
        if back:
            return reverse_lazy('estudios:estudio_detail', kwargs={'pk': back})
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class HistorialLaboralUpdateView(LoginRequiredMixin, UpdateView):
    model = HistorialLaboral
    form_class = HistorialLaboralForm
    success_url = reverse_lazy('laboral:historiallaboral_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class HistorialLaboralDeleteView(LoginRequiredMixin, DeleteView):
    model = HistorialLaboral
    context_object_name = 'historial_laboral'
    success_url = reverse_lazy('laboral:historiallaboral_list')
