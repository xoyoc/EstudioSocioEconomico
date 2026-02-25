from django.urls import path

from . import views

app_name = 'laboral'

urlpatterns = [
    path('', views.HistorialLaboralListView.as_view(), name='historiallaboral_list'),
    path('crear/', views.HistorialLaboralCreateView.as_view(), name='historiallaboral_create'),
    path('<int:pk>/', views.HistorialLaboralDetailView.as_view(), name='historiallaboral_detail'),
    path('<int:pk>/editar/', views.HistorialLaboralUpdateView.as_view(), name='historiallaboral_update'),
    path('<int:pk>/eliminar/', views.HistorialLaboralDeleteView.as_view(), name='historiallaboral_delete'),
    path('<int:pk>/verificar/', views.VerificarHistorialLaboralView.as_view(), name='historiallaboral_verificar'),
]
