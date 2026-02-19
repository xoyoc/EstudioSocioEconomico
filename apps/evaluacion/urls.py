from django.urls import path

from . import views

app_name = 'evaluacion'

urlpatterns = [
    path('', views.EvaluacionRiesgoListView.as_view(), name='evaluacionriesgo_list'),
    path('crear/', views.EvaluacionRiesgoCreateView.as_view(), name='evaluacionriesgo_create'),
    path('<int:pk>/', views.EvaluacionRiesgoDetailView.as_view(), name='evaluacionriesgo_detail'),
    path('<int:pk>/editar/', views.EvaluacionRiesgoUpdateView.as_view(), name='evaluacionriesgo_update'),
    path('<int:pk>/eliminar/', views.EvaluacionRiesgoDeleteView.as_view(), name='evaluacionriesgo_delete'),
]
