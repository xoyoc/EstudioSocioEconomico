from django.urls import path

from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.NotificacionListView.as_view(), name='notificacion_list'),
    path('crear/', views.NotificacionCreateView.as_view(), name='notificacion_create'),
    path('<int:pk>/', views.NotificacionDetailView.as_view(), name='notificacion_detail'),
    path('<int:pk>/editar/', views.NotificacionUpdateView.as_view(), name='notificacion_update'),
    path('<int:pk>/eliminar/', views.NotificacionDeleteView.as_view(), name='notificacion_delete'),
]
