from django.urls import path

from . import views

app_name = 'domicilios'

urlpatterns = [
    path('', views.DomicilioListView.as_view(), name='domicilio_list'),
    path('crear/', views.DomicilioCreateView.as_view(), name='domicilio_create'),
    path('<int:pk>/', views.DomicilioDetailView.as_view(), name='domicilio_detail'),
    path('<int:pk>/editar/', views.DomicilioUpdateView.as_view(), name='domicilio_update'),
    path('<int:pk>/eliminar/', views.DomicilioDeleteView.as_view(), name='domicilio_delete'),
]
