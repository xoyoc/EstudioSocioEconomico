from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import SituacionEconomica


class SituacionEconomicaListView(ListView):
    model = SituacionEconomica
    context_object_name = 'situaciones_economicas'


class SituacionEconomicaDetailView(DetailView):
    model = SituacionEconomica
    context_object_name = 'situacion_economica'


class SituacionEconomicaCreateView(CreateView):
    model = SituacionEconomica
    fields = [
        'estudio',
        'salario_mensual', 'bonos_comisiones', 'ingresos_extra',
        'apoyo_familiar', 'otros_ingresos', 'descripcion_otros_ingresos',
        'gasto_alimentacion', 'gasto_vivienda', 'gasto_servicios',
        'gasto_transporte', 'gasto_educacion', 'gasto_salud',
        'gasto_deudas', 'otros_gastos', 'descripcion_otros_gastos',
        'tiene_automovil', 'automovil_marca_modelo', 'automovil_anio',
        'patrimonio_inmobiliario', 'descripcion_patrimonio',
        'tiene_creditos', 'credito_hipotecario', 'credito_automotriz',
        'tarjetas_credito', 'prestamos_personales',
        'otros_creditos', 'descripcion_otros_creditos',
    ]
    success_url = reverse_lazy('economia:situacioneconomica_list')


class SituacionEconomicaUpdateView(UpdateView):
    model = SituacionEconomica
    fields = [
        'estudio',
        'salario_mensual', 'bonos_comisiones', 'ingresos_extra',
        'apoyo_familiar', 'otros_ingresos', 'descripcion_otros_ingresos',
        'gasto_alimentacion', 'gasto_vivienda', 'gasto_servicios',
        'gasto_transporte', 'gasto_educacion', 'gasto_salud',
        'gasto_deudas', 'otros_gastos', 'descripcion_otros_gastos',
        'tiene_automovil', 'automovil_marca_modelo', 'automovil_anio',
        'patrimonio_inmobiliario', 'descripcion_patrimonio',
        'tiene_creditos', 'credito_hipotecario', 'credito_automotriz',
        'tarjetas_credito', 'prestamos_personales',
        'otros_creditos', 'descripcion_otros_creditos',
    ]
    success_url = reverse_lazy('economia:situacioneconomica_list')


class SituacionEconomicaDeleteView(DeleteView):
    model = SituacionEconomica
    context_object_name = 'situacion_economica'
    success_url = reverse_lazy('economia:situacioneconomica_list')
