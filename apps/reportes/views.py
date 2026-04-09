import io
import json
import urllib.parse
import urllib.request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from apps.estudios.models import EstudioSocioeconomico

# Estados en los que el PDF puede generarse
ESTADOS_PERMITIDOS = ('COM', 'REV', 'APR', 'REC')


def _geocodificar_nominatim(domicilio):
    """
    Geocodifica un Domicilio usando Nominatim (OpenStreetMap).
    Gratuito, sin API key. Retorna (lat, lon) como floats, o (None, None).
    """
    query = (
        f"{domicilio.calle} {domicilio.numero_exterior}, "
        f"{domicilio.colonia}, {domicilio.municipio}, "
        f"{domicilio.estado}, México"
    )
    params = urllib.parse.urlencode({
        'q': query,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'mx',
    })
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'EstudioEcoNom/2.0 (sistema interno)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception:
        pass
    return None, None


def _url_mapa(lat, lon):
    """
    Construye la URL del mapa estático según el servicio configurado.
    Prioridad: Google Maps → Mapbox → OpenStreetMap (sin API key).
    """
    from django.conf import settings

    google_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    mapbox_key = getattr(settings, 'MAPBOX_API_KEY', '')

    if google_key:
        # Google Maps Static API
        # https://developers.google.com/maps/documentation/maps-static/overview
        params = urllib.parse.urlencode({
            'center': f'{lat},{lon}',
            'zoom': 16,
            'size': '600x300',
            'markers': f'color:red|{lat},{lon}',
            'maptype': 'roadmap',
            'key': google_key,
        })
        return f"https://maps.googleapis.com/maps/api/staticmap?{params}", 'google'

    if mapbox_key:
        # Mapbox Static Images API
        # https://docs.mapbox.com/api/maps/static-images/
        marker = f'pin-s+FF0000({lon},{lat})'
        return (
            f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
            f"/{marker}/{lon},{lat},16/600x300"
            f"?access_token={mapbox_key}"
        ), 'mapbox'

    # OpenStreetMap (sin API key — puede ser inestable)
    return (
        f"https://staticmap.openstreetmap.de/staticmap.php"
        f"?center={lat},{lon}&zoom=16&size=600x300"
        f"&markers={lat},{lon},red-pushpin"
    ), 'osm'


def _descargar_imagen_mapa(lat, lon):
    """
    Descarga el mapa estático y lo retorna como data URL base64.
    WeasyPrint y el navegador no necesitan hacer peticiones externas al renderizar.
    Retorna None si falla la descarga.
    """
    import base64

    url, _ = _url_mapa(lat, lon)
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'EstudioEcoNom/2.0 (sistema interno)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content_type = resp.headers.get('Content-Type', 'image/png').split(';')[0]
            b64 = base64.b64encode(resp.read()).decode('ascii')
            return f"data:{content_type};base64,{b64}"
    except Exception:
        return None


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

    # Fotos: busca por persona (el FK estudio puede ser null)
    from apps.documentos.models import Documento
    FOTOS_TIPOS = list(Documento.FOTOS_TIPOS)
    fotos_qs = Documento.objects.filter(
        persona=persona, tipo__in=FOTOS_TIPOS
    ).order_by('tipo', 'created_at')
    foto_selfie = fotos_qs.filter(tipo='FSE').first()
    fotos = fotos_qs.exclude(tipo='FSE')

    # Empresa cliente
    empresa = estudio.empresa_cliente

    # ─── GEOLOCALIZACIÓN PARA EL CROQUIS (3 fuentes en cascada) ─────────────
    # Fuente 1: visita domiciliaria con GPS (más preciso — inspector en el lugar)
    mapa_url = None
    origen_coordenadas = None
    _lat = _lon = None

    if visita_principal and visita_principal.latitud and visita_principal.longitud:
        _lat = float(visita_principal.latitud)
        _lon = float(visita_principal.longitud)
        origen_coordenadas = 'visita'

    # Fuente 2: coordenadas guardadas en el domicilio (capturadas por el candidato en paso_2)
    elif domicilio_actual and domicilio_actual.latitud and domicilio_actual.longitud:
        _lat = float(domicilio_actual.latitud)
        _lon = float(domicilio_actual.longitud)
        origen_coordenadas = 'domicilio'

    # Fuente 3: geocodificación desde la dirección vía Nominatim (OpenStreetMap, sin API key)
    elif domicilio_actual:
        _lat, _lon = _geocodificar_nominatim(domicilio_actual)
        if _lat and _lon:
            origen_coordenadas = 'geocodificado'

    # Con las coordenadas resueltas, descargar la imagen y embeber como base64
    if _lat and _lon:
        mapa_url = _descargar_imagen_mapa(_lat, _lon)
        if not mapa_url:
            # Si falla la descarga, dejar sin mapa (no romper el reporte)
            origen_coordenadas = None
    # ─────────────────────────────────────────────────────────────────────────

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
        'foto_selfie': foto_selfie,
        'fotos': fotos,
        'mapa_url': mapa_url,
        'origen_coordenadas': origen_coordenadas,  # 'visita' | 'domicilio' | 'geocodificado' | None
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
