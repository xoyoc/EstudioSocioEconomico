from django.urls import path

from . import views

app_name = 'familia'

urlpatterns = [
    path('', views.GrupoFamiliarListView.as_view(), name='grupofamiliar_list'),
    path('crear/', views.GrupoFamiliarCreateView.as_view(), name='grupofamiliar_create'),
    path('<int:pk>/', views.GrupoFamiliarDetailView.as_view(), name='grupofamiliar_detail'),
    path('<int:pk>/editar/', views.GrupoFamiliarUpdateView.as_view(), name='grupofamiliar_update'),
    path('<int:pk>/eliminar/', views.GrupoFamiliarDeleteView.as_view(), name='grupofamiliar_delete'),
]
