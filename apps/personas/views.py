from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .forms import PersonaForm, SaludPersonaForm
from .models import Persona, SaludPersona


class PersonaListView(LoginRequiredMixin, ListView):
    model = Persona
    context_object_name = 'personas'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(
                Q(folio__icontains=q) | Q(nombre__icontains=q) |
                Q(apellido_paterno__icontains=q) | Q(apellido_materno__icontains=q) |
                Q(curp__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class PersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    context_object_name = 'persona'


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    success_url = reverse_lazy('personas:persona_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    success_url = reverse_lazy('personas:persona_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    context_object_name = 'persona'
    success_url = reverse_lazy('personas:persona_list')


class SaludPersonaCreateView(LoginRequiredMixin, CreateView):
    model = SaludPersona
    form_class = SaludPersonaForm
    success_url = reverse_lazy('personas:persona_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SaludPersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = SaludPersona
    form_class = SaludPersonaForm
    context_object_name = 'salud'
    success_url = reverse_lazy('personas:persona_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
