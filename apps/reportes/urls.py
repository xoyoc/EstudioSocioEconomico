from django.urls import path

from . import views

app_name = 'reportes'

urlpatterns = [
    path('estudio/<int:pk>/preview/', views.VistaPreviewReporteView.as_view(), name='estudio_preview'),
    path('estudio/<int:pk>/pdf/', views.GenerarReportePDFView.as_view(), name='estudio_pdf'),
]
