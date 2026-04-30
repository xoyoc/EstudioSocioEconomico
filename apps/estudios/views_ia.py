import json

import openai
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import EstudioSocioeconomico

# DigitalOcean AI Platform — compatible con OpenAI SDK
DO_AI_BASE_URL = "https://inference.do-ai.run/v1"

# Modelos disponibles con el DO_MODEL_ACCESS_KEY actual:
#   meta-llama/Llama-4-Maverick-17B-128E-Instruct
#   meta-llama/Llama-3.3-70B-Instruct
#   deepseek-ai/DeepSeek-V3
#   deepseek-ai/DeepSeek-R1-Distill-Llama-70B
DO_AI_MODEL = "meta-llama/Llama-4-Maverick-17B-128E-Instruct"


def _cliente_ia():
    return openai.OpenAI(
        base_url=DO_AI_BASE_URL,
        api_key=settings.DO_MODEL_ACCESS_KEY,
    )


def _recopilar_datos_estudio(estudio):
    """Reúne todos los datos del estudio en un texto estructurado para el prompt."""
    p = estudio.persona
    lineas = []

    # Datos personales
    lineas.append(f"CANDIDATO: {p.nombre_completo}")
    if p.fecha_nacimiento:
        from datetime import date
        edad = (date.today() - p.fecha_nacimiento).days // 365
        lineas.append(f"Edad: {edad} años")
    lineas.append(f"Estado civil: {p.get_estado_civil_display()}")
    lineas.append(f"Número de dependientes: {p.numero_dependientes}")
    if p.lugar_nacimiento:
        lineas.append(f"Lugar de nacimiento: {p.lugar_nacimiento}")

    # Estudio
    lineas.append(f"\nESTUDIO: {estudio.tipo_estudio.nombre if estudio.tipo_estudio else 'N/A'}")
    lineas.append(f"Estado: {estudio.get_estado_display()}")
    if estudio.empresa_cliente:
        lineas.append(f"Empresa solicitante: {estudio.empresa_cliente.nombre}")

    # Domicilio actual
    domicilio = p.domicilios.filter(tipo='ACT').first()
    if domicilio:
        lineas.append(f"\nDOMICILIO ACTUAL:")
        lineas.append(f"  Tipo de vivienda: {domicilio.get_tipo_vivienda_display() if domicilio.tipo_vivienda else 'No especificado'}")
        lineas.append(f"  Tipo de inmueble: {domicilio.get_tipo_inmueble_display() if domicilio.tipo_inmueble else 'No especificado'}")
        if domicilio.tiempo_residencia_anios is not None:
            lineas.append(f"  Tiempo de residencia: {domicilio.tiempo_residencia_anios} años {domicilio.tiempo_residencia_meses or 0} meses")
        servicios = []
        if domicilio.tiene_agua: servicios.append("agua")
        if domicilio.tiene_luz: servicios.append("luz")
        if domicilio.tiene_drenaje: servicios.append("drenaje")
        if domicilio.tiene_gas: servicios.append("gas")
        if domicilio.tiene_internet: servicios.append("internet")
        if servicios:
            lineas.append(f"  Servicios: {', '.join(servicios)}")

    # Educación
    educacion_qs = p.educacion.all().select_related('nivel').order_by('-anio_fin')
    if educacion_qs.exists():
        lineas.append(f"\nEDUCACIÓN:")
        for ed in educacion_qs[:3]:
            lineas.append(f"  - {ed.nivel.nivel}: {ed.titulo} en {ed.institucion} ({ed.get_estado_display()})")

    # Idiomas
    idiomas = p.idiomas.all()
    if idiomas.exists():
        lineas.append(f"  Idiomas: {', '.join([f'{i.idioma} (habla {i.porcentaje_habla}%)' for i in idiomas])}")

    # Salud
    try:
        salud = p.salud
        lineas.append(f"\nSALUD: {salud.get_nivel_salud_display() if salud.nivel_salud else 'No especificado'}")
        if salud.enfermedades_cronicas:
            lineas.append(f"  Enfermedades/condiciones: {salud.enfermedades_cronicas[:200]}")
    except Exception:
        pass

    # Historial laboral
    laboral_qs = p.historial_laboral.all().order_by('-fecha_inicio')
    if laboral_qs.exists():
        lineas.append(f"\nHISTORIAL LABORAL:")
        for emp in laboral_qs[:4]:
            estado_lab = "Trabajo actual" if emp.es_trabajo_actual else f"Hasta {emp.fecha_fin}"
            verificado = "✓ verificado" if emp.verificada else ""
            lineas.append(f"  - {emp.puesto} en {emp.empresa} ({emp.fecha_inicio} – {estado_lab}) {verificado}")
            lineas.append(f"    Salario: ${emp.salario_final:,.0f}")

    # Grupo familiar
    familia_qs = p.grupo_familiar.all()
    if familia_qs.exists():
        dependientes_totales = familia_qs.filter(tipo_dependencia='TOT').count()
        aportan = familia_qs.filter(aporta_ingreso=True).count()
        lineas.append(f"\nGRUPO FAMILIAR: {familia_qs.count()} integrantes")
        lineas.append(f"  Dependientes económicos totales: {dependientes_totales}")
        lineas.append(f"  Miembros que aportan ingreso: {aportan}")

    # Situación económica
    try:
        eco = estudio.situacion_economica
        lineas.append(f"\nSITUACIÓN ECONÓMICA:")
        lineas.append(f"  Ingreso mensual total: ${eco.ingreso_total_mensual:,.0f}")
        lineas.append(f"  Egreso mensual total: ${eco.egreso_total_mensual:,.0f}")
        lineas.append(f"  Capacidad de ahorro: ${eco.capacidad_ahorro:,.0f}")
        lineas.append(f"  Percepción económica: {eco.get_situacion_economica_percibida_display() if eco.situacion_economica_percibida else 'N/A'}")
        if eco.tiene_creditos:
            creditos = []
            if eco.tiene_credito_hipotecario: creditos.append("hipotecario")
            if eco.tiene_credito_automotriz: creditos.append("automotriz")
            if eco.tiene_tarjeta_credito: creditos.append("tarjeta de crédito")
            if eco.tiene_credito_personal: creditos.append("personal")
            if creditos:
                lineas.append(f"  Créditos activos: {', '.join(creditos)}")
        if eco.tiene_automovil:
            lineas.append(f"  Automóvil: {eco.automovil_marca_modelo or 'Sí'} ({eco.automovil_anio or 'N/A'})")
    except Exception:
        pass

    # Referencias
    referencias_qs = p.referencias.all()
    if referencias_qs.exists():
        verificadas = referencias_qs.filter(verificada=True).count()
        lineas.append(f"\nREFERENCIAS: {referencias_qs.count()} registradas, {verificadas} verificadas")

    # Visita domiciliaria
    visita = estudio.visitas.order_by('-fecha_visita').first()
    if visita:
        lineas.append(f"\nVISITA DOMICILIARIA:")
        lineas.append(f"  Tipo de zona: {visita.get_tipo_zona_display() if visita.tipo_zona else 'N/A'}")
        lineas.append(f"  Nivel de seguridad: {visita.nivel_seguridad}/5")
        lineas.append(f"  Persona encontrada: {'Sí' if visita.persona_encontrada else 'No'}")
        lineas.append(f"  Domicilio verificado: {'Sí' if visita.verificacion_domicilio else 'No'}")
        if visita.observaciones_generales:
            lineas.append(f"  Observaciones: {visita.observaciones_generales[:300]}")

    return "\n".join(lineas)


class AnalizarEstudioIAView(LoginRequiredMixin, View):
    """Genera y guarda aspectos_positivos, aspectos_negativos y conclusion usando DigitalOcean AI."""

    def post(self, request, pk):
        estudio = get_object_or_404(EstudioSocioeconomico, pk=pk)

        if not settings.DO_MODEL_ACCESS_KEY:
            return JsonResponse({'error': 'API key de DigitalOcean AI no configurada.'}, status=503)

        datos = _recopilar_datos_estudio(estudio)

        prompt = f"""Eres un analista experto en estudios socioeconómicos para empresas en México.
Basándote en los siguientes datos del candidato, genera un análisis profesional en español mexicano.

{datos}

Responde ÚNICAMENTE con un objeto JSON válido con exactamente estas tres claves (sin texto adicional, sin markdown, sin bloques de código):
{{
  "aspectos_positivos": "Redacta 2-4 oraciones sobre los puntos fuertes del perfil del candidato.",
  "aspectos_negativos": "Redacta 2-4 oraciones sobre áreas de oportunidad o factores de atención. Si no hay aspectos negativos relevantes, escribe 'Sin comentarios'.",
  "conclusion": "Redacta 2-5 oraciones con la conclusión general del estudio, incluyendo si el candidato cumple con el perfil solicitado."
}}

Usa lenguaje formal, profesional y en tercera persona. Menciona el nombre del candidato en la conclusión."""

        try:
            cliente = _cliente_ia()
            respuesta = cliente.chat.completions.create(
                model=DO_AI_MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            texto = respuesta.choices[0].message.content.strip()

            # Extraer JSON del response (algunos modelos añaden markdown)
            inicio = texto.find('{')
            fin = texto.rfind('}') + 1
            datos_json = json.loads(texto[inicio:fin])

            # Guardar en el estudio
            estudio.aspectos_positivos = datos_json.get('aspectos_positivos', '')
            estudio.aspectos_negativos = datos_json.get('aspectos_negativos', '')
            estudio.conclusion = datos_json.get('conclusion', '')
            estudio.updated_by = request.user
            estudio.save(update_fields=['aspectos_positivos', 'aspectos_negativos', 'conclusion', 'updated_by', 'updated_at'])

            return JsonResponse({
                'ok': True,
                'aspectos_positivos': estudio.aspectos_positivos,
                'aspectos_negativos': estudio.aspectos_negativos,
                'conclusion': estudio.conclusion,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'La IA devolvió un formato inesperado. Intenta de nuevo.'}, status=500)
        except openai.APIError as exc:
            return JsonResponse({'error': f'Error al conectar con DigitalOcean AI: {exc}'}, status=502)


class SugerirEvaluacionIAView(LoginRequiredMixin, View):
    """Sugiere puntuaciones y análisis cualitativo para EvaluacionRiesgo usando DigitalOcean AI."""

    def post(self, request, pk):
        estudio = get_object_or_404(EstudioSocioeconomico, pk=pk)

        if not settings.DO_MODEL_ACCESS_KEY:
            return JsonResponse({'error': 'API key de DigitalOcean AI no configurada.'}, status=503)

        datos = _recopilar_datos_estudio(estudio)

        prompt = f"""Eres un evaluador experto en riesgo socioeconómico para empresas en México.
Basándote en los siguientes datos del candidato, asigna una puntuación del 0 al 100 a cada categoría de riesgo y proporciona un análisis cualitativo en español mexicano.

{datos}

Criterios de puntuación por categoría (0-100):
- 80-100: Excelente, sin factores de riesgo
- 60-79: Bueno, factores menores
- 40-59: Regular, factores moderados que requieren atención
- 0-39: Deficiente, factores de riesgo importantes

Categorías:
1. identificacion: Veracidad y vigencia de documentos de identidad, CURP, RFC
2. domicilio: Estabilidad domiciliaria, características del inmueble, tiempo de residencia
3. laboral: Estabilidad laboral, trayectoria, verificación de empleos
4. economica: Equilibrio ingresos/egresos, capacidad de ahorro, patrimonio
5. crediticia: Manejo de créditos y deudas, nivel de endeudamiento
6. referencias: Calidad y verificación de referencias personales/laborales

Responde ÚNICAMENTE con un objeto JSON válido (sin texto adicional, sin markdown, sin bloques de código):
{{
  "puntuacion_identificacion": <número 0-100>,
  "puntuacion_domicilio": <número 0-100>,
  "puntuacion_laboral": <número 0-100>,
  "puntuacion_economica": <número 0-100>,
  "puntuacion_crediticia": <número 0-100>,
  "puntuacion_referencias": <número 0-100>,
  "factores_riesgo": "Describe los principales factores de riesgo identificados en 2-4 oraciones.",
  "factores_atenuantes": "Describe los factores que reducen el riesgo en 2-4 oraciones.",
  "recomendacion_final": "Proporciona la recomendación final en 2-4 oraciones, incluyendo si se sugiere aprobar o no al candidato."
}}"""

        try:
            cliente = _cliente_ia()
            respuesta = cliente.chat.completions.create(
                model=DO_AI_MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            texto = respuesta.choices[0].message.content.strip()

            inicio = texto.find('{')
            fin = texto.rfind('}') + 1
            datos_json = json.loads(texto[inicio:fin])

            # Normalizar puntuaciones al rango 0-100
            campos_num = [
                'puntuacion_identificacion', 'puntuacion_domicilio',
                'puntuacion_laboral', 'puntuacion_economica',
                'puntuacion_crediticia', 'puntuacion_referencias',
            ]
            for campo in campos_num:
                if campo in datos_json:
                    datos_json[campo] = max(0, min(100, int(datos_json[campo])))

            return JsonResponse({'ok': True, **datos_json})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'La IA devolvió un formato inesperado. Intenta de nuevo.'}, status=500)
        except openai.APIError as exc:
            return JsonResponse({'error': f'Error al conectar con DigitalOcean AI: {exc}'}, status=502)
