from django.urls import path

from . import views

app_name = 'referencias'

urlpatterns = [
    path('', views.ReferenciaListView.as_view(), name='referencia_list'),
    path('crear/', views.ReferenciaCreateView.as_view(), name='referencia_create'),
    path('<int:pk>/', views.ReferenciaDetailView.as_view(), name='referencia_detail'),
    path('<int:pk>/editar/', views.ReferenciaUpdateView.as_view(), name='referencia_update'),
    path('<int:pk>/eliminar/', views.ReferenciaDeleteView.as_view(), name='referencia_delete'),
    path('<int:pk>/verificar/', views.VerificarReferenciaView.as_view(), name='referencia_verificar'),
]
