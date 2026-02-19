from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('configuracion/', include('apps.configuracion.urls')),
    path('personas/', include('apps.personas.urls')),
    path('estudios/', include('apps.estudios.urls')),
    path('domicilios/', include('apps.domicilios.urls')),
    path('economia/', include('apps.economia.urls')),
    path('educacion/', include('apps.educacion.urls')),
    path('laboral/', include('apps.laboral.urls')),
    path('familia/', include('apps.familia.urls')),
    path('referencias/', include('apps.referencias.urls')),
    path('visitas/', include('apps.visitas.urls')),
    path('evaluacion/', include('apps.evaluacion.urls')),
    path('documentos/', include('apps.documentos.urls')),
    path('notificaciones/', include('apps.notificaciones.urls')),
]
