from django.urls import path

from . import views

app_name = 'visitas'

urlpatterns = [
    path('', views.VisitaDomiciliariaListView.as_view(), name='visitadomiciliaria_list'),
    path('crear/', views.VisitaDomiciliariaCreateView.as_view(), name='visitadomiciliaria_create'),
    path('<int:pk>/', views.VisitaDomiciliariaDetailView.as_view(), name='visitadomiciliaria_detail'),
    path('<int:pk>/editar/', views.VisitaDomiciliariaUpdateView.as_view(), name='visitadomiciliaria_update'),
    path('<int:pk>/eliminar/', views.VisitaDomiciliariaDeleteView.as_view(), name='visitadomiciliaria_delete'),
]
