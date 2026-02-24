"""URL routes for the public candidate self-service portal (accessed via EstudioToken UUID)."""
from django.urls import path

from . import views_candidato

app_name = 'candidato'

urlpatterns = [
    path('<uuid:token>/', views_candidato.BienvenidaView.as_view(), name='bienvenida'),
    path('<uuid:token>/paso/<int:n>/', views_candidato.PasoDispatcherView.as_view(), name='paso'),
    path('<uuid:token>/gracias/', views_candidato.GraciasView.as_view(), name='gracias'),
    path('<uuid:token>/invalido/', views_candidato.TokenInvalidoView.as_view(), name='token_invalido'),
]
