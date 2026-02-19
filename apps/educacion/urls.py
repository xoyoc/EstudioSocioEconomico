from django.urls import path

from . import views

app_name = 'educacion'

urlpatterns = [
    # NivelEducativo
    path('niveles/', views.NivelEducativoListView.as_view(), name='niveleducativo_list'),
    path('niveles/crear/', views.NivelEducativoCreateView.as_view(), name='niveleducativo_create'),
    path('niveles/<int:pk>/', views.NivelEducativoDetailView.as_view(), name='niveleducativo_detail'),
    path('niveles/<int:pk>/editar/', views.NivelEducativoUpdateView.as_view(), name='niveleducativo_update'),
    path('niveles/<int:pk>/eliminar/', views.NivelEducativoDeleteView.as_view(), name='niveleducativo_delete'),

    # Educacion
    path('', views.EducacionListView.as_view(), name='educacion_list'),
    path('crear/', views.EducacionCreateView.as_view(), name='educacion_create'),
    path('<int:pk>/', views.EducacionDetailView.as_view(), name='educacion_detail'),
    path('<int:pk>/editar/', views.EducacionUpdateView.as_view(), name='educacion_update'),
    path('<int:pk>/eliminar/', views.EducacionDeleteView.as_view(), name='educacion_delete'),
]
