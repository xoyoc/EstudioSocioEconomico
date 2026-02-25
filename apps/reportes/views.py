import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from apps.estudios.models import EstudioSocioeconomico

# Estados en los que el PDF puede generarse
ESTADOS_PERMITIDOS = ('COM', 'REV', 'APR', 'REC')


def _get_contexto_pdf(estudio):
    """Reúne todo el contexto necesario para renderizar el reporte."""
    persona = estudio.persona

    # Domicilio actual
    domicilio_actual = persona.domicilios.filter(tipo='ACT').first()

    # Educación (ordenada por nivel)
    educacion = persona.educacion.select_related('nivel').order_by('-anio_inicio')

    # Idiomas
    idiomas = persona.idiomas.all()

    # Salud
    salud = getattr(persona, 'salud', None)

    # Grupo familiar
    familia = persona.grupo_familiar.all()

    # Situación económica (OneToOne con el estudio)
    try:
        economia = estudio.situacion_economica
    except Exception:
        economia = None

    # Historial laboral
    laboral = persona.historial_laboral.order_by('-fecha_inicio')

    # Referencias
    referencias = persona.referencias.all()

    # Visitas (toma la más reciente con GPS para el croquis)
    visitas = estudio.visitas.order_by('-fecha_visita')
    visita_principal = visitas.filter(
        latitud__isnull=False, longitud__isnull=False
    ).first() or visitas.first()

    # Evaluación de riesgo
    try:
        evaluacion = estudio.evaluacion_riesgo
    except Exception:
        evaluacion = None

    # Documentos tipo FOT (fotos)
    fotos = estudio.documentos.filter(tipo='FOT').select_related('persona')

    # Empresa cliente
    empresa = estudio.empresa_cliente

    # URL de mapa estático OpenStreetMap (gratuito, sin API key)
    mapa_url = None
    if visita_principal and visita_principal.latitud and visita_principal.longitud:
        lat = float(visita_principal.latitud)
        lon = float(visita_principal.longitud)
        mapa_url = (
            f"https://staticmap.openstreetmap.de/staticmap.php"
            f"?center={lat},{lon}&zoom=16&size=600x300"
            f"&markers={lat},{lon},red-pushpin"
        )

    return {
        'estudio': estudio,
        'persona': persona,
        'empresa': empresa,
        'domicilio_actual': domicilio_actual,
        'educacion': educacion,
        'idiomas': idiomas,
        'salud': salud,
        'familia': familia,
        'economia': economia,
        'laboral': laboral,
        'referencias': referencias,
        'visitas': visitas,
        'visita_principal': visita_principal,
        'evaluacion': evaluacion,
        'fotos': fotos,
        'mapa_url': mapa_url,
        'fecha_generacion': timezone.now(),
    }


class VistaPreviewReporteView(LoginRequiredMixin, View):
    """Renderiza el HTML del reporte para vista previa en el navegador."""

    def get(self, request, pk):
        estudio = get_object_or_404(EstudioSocioeconomico, pk=pk)
        ctx = _get_contexto_pdf(estudio)
        html = render_to_string('reportes/estudio_pdf.html', ctx, request=request)
        return HttpResponse(html)


class GenerarReportePDFView(LoginRequiredMixin, View):
    """Genera y descarga el PDF del estudio usando WeasyPrint."""

    def get(self, request, pk):
        from weasyprint import HTML, CSS

        estudio = get_object_or_404(EstudioSocioeconomico, pk=pk)
        ctx = _get_contexto_pdf(estudio)

        html_string = render_to_string('reportes/estudio_pdf.html', ctx, request=request)

        pdf_buffer = io.BytesIO()
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        fecha_str = timezone.now().strftime('%Y%m%d')
        folio = estudio.persona.folio
        filename = f"Estudio_{folio}_{fecha_str}.pdf"

        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
