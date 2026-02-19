from django.urls import path

from . import views

app_name = 'economia'

urlpatterns = [
    path('', views.SituacionEconomicaListView.as_view(), name='situacioneconomica_list'),
    path('crear/', views.SituacionEconomicaCreateView.as_view(), name='situacioneconomica_create'),
    path('<int:pk>/', views.SituacionEconomicaDetailView.as_view(), name='situacioneconomica_detail'),
    path('<int:pk>/editar/', views.SituacionEconomicaUpdateView.as_view(), name='situacioneconomica_update'),
    path('<int:pk>/eliminar/', views.SituacionEconomicaDeleteView.as_view(), name='situacioneconomica_delete'),
]
