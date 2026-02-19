from django.urls import path

from . import views

app_name = 'configuracion'

urlpatterns = [
    path('', views.TipoEstudioListView.as_view(), name='tipoestudio_list'),
    path('crear/', views.TipoEstudioCreateView.as_view(), name='tipoestudio_create'),
    path('<int:pk>/', views.TipoEstudioDetailView.as_view(), name='tipoestudio_detail'),
    path('<int:pk>/editar/', views.TipoEstudioUpdateView.as_view(), name='tipoestudio_update'),
    path('<int:pk>/eliminar/', views.TipoEstudioDeleteView.as_view(), name='tipoestudio_delete'),
]
