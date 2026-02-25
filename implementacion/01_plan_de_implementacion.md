# Plan de Implementación — EstudioEcoNom (Meraki)

**Versión:** 1.1
**Fecha:** 2026-02-21
**Objetivo:** Digitalizar el proceso de estudio socioeconómico de Meraki Consultoría generando un reporte PDF idéntico al formato actual, soportando dos escenarios de captura de datos.

---

## Dos escenarios de operación

```
┌─────────────────────────────────────────────────────────┐
│  ESCENARIO A — Autogestión del candidato                │
│                                                         │
│  Analista crea estudio → genera link con token →        │
│  Candidato llena portal desde su celular →              │
│  Sube fotos y documentos →                              │
│  Analista revisa, complementa y genera PDF              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  ESCENARIO B — Inspector en campo                       │
│                                                         │
│  Analista crea estudio y agenda visita →                │
│  Inspector va al domicilio (app mobile-first) →         │
│  Toma fotos, captura GPS, evalúa entorno →              │
│  Hace llamadas a referencias y jefes →                  │
│  Analista revisa y genera PDF                           │
└─────────────────────────────────────────────────────────┘
```

---

## Estructura del reporte PDF de referencia

El reporte final consta de 8 páginas:

| Pág. | Sección | Datos |
|------|---------|-------|
| 1 | Portada + foto + Comentarios y conclusiones | Header empresa, folio, fechas, narrativo |
| 2 | Datos personales + Identificaciones + Datos escolares | Persona, documentos oficiales, Educacion |
| 3 | Hábitos y salud + Familiares directos | SaludPersona, GrupoFamiliar |
| 4 | Datos del inmueble + Patrimonio + Situación económica | Domicilio, SituacionEconomica |
| 5 | Referencias + Comentarios de colonos + Observaciones | Referencia, VisitaDomiciliaria |
| 6 | Croquis de domicilio (mapa estático) | GPS de VisitaDomiciliaria |
| 7-8 | Fotografías del domicilio (fachada e interior) | Documento tipo FOT |

---

## FASE 0 — Completar modelos (base de datos al 100%)

**Estado:** ✅ Completada
**Prioridad:** 🔴 Crítico
**Dependencias:** Ninguna

### Objetivo
Alinear completamente la base de datos con el reporte PDF de referencia. Los modelos actuales están incompletos para generar el reporte final.

### Campos faltantes detectados en el PDF

**`apps/referencias/models.py` — modelo `Referencia`:**
- [x] `actividad_tiempo_libre` — TextField, blank — Qué hace la referencia en su tiempo libre
- [x] `lugares_laborado` — TextField, blank — Donde ha trabajado la referencia
- [x] `conducta` — TextField, blank — Descripción de conducta
- [x] `cualidades` — TextField, blank — Cualidades destacadas

**`apps/visitas/models.py` — modelo `VisitaDomiciliaria`:**
- [x] `comentarios_colonos` — TextField, blank — Comentarios de vecinos al momento de visita

**`apps/estudios/models.py` — modelo `EstudioSocioeconomico`:**
- [x] `aspectos_positivos` — TextField, blank — Aspectos positivos del candidato
- [x] `aspectos_negativos` — TextField, blank — Aspectos negativos del candidato

**`apps/domicilios/models.py` — modelo `Domicilio`:**
- [x] `observaciones_inmueble` — TextField, blank — Observaciones y comentarios del inmueble

### Nuevo modelo: `EmpresaCliente`

El reporte incluye el logo y nombre de la empresa que contrató el estudio (p. ej. Hutchison Ports LCT). Creado en `apps/configuracion/`.

- [x] Crear modelo `EmpresaCliente` (nombre, logo, activo, created_at)
- [x] Agregar FK `empresa_cliente` (null=True) a `EstudioSocioeconomico`
- [x] Registrar en admin con upload de logo

### Nuevo modelo: `EstudioToken` (para Escenario A)

- [x] Crear modelo `EstudioToken` en `apps/estudios/` (token UUID, activo, fecha_expiracion, vigente property)
- [x] Registrar en admin

### Tareas de esta fase
- [x] Modificar modelos con campos faltantes
- [x] Ejecutar `makemigrations && migrate`
- [x] Actualizar admin de `referencias`, `visitas`, `estudios`, `domicilios`, `configuracion`
- [x] Instalar Pillow (requerido por ImageField)
- [ ] Actualizar `CONTEXT.md` con los nuevos campos (pendiente)

---

## FASE 1 — Base de templates y autenticación

**Estado:** ✅ Completada (componentes opcionales pendientes)
**Prioridad:** 🔴 Crítico
**Dependencias:** FASE 0

### Objetivo
Sistema funcional con autenticación, navegación y estructura visual base.

### Configuración técnica
- [x] Agregar `MEDIA_ROOT = BASE_DIR / 'media'` y `MEDIA_URL = 'media/'` a `settings.py`
- [x] Agregar `STATIC_ROOT = BASE_DIR / 'staticfiles'` a `settings.py`
- [x] Agregar URL de media en `esteconom/urls.py` (solo cuando `DEBUG=True`)
- [x] Crear `apps/estudios/urls_candidato.py` (placeholder para Escenario A)
- [x] Instalar HTMX en `base.html`: `<script src="https://unpkg.com/htmx.org@1.9.12"></script>`
- [x] Agregar `paginate_by = 25` a todas las `ListView` (13 apps)
- [x] Agregar `LoginRequiredMixin` a todas las vistas (13 apps)
- [x] Implementar patrón `form_valid()` con `created_by` / `updated_by` en todas las CreateView/UpdateView
- [x] Actualizar `fields` en vistas para incluir todos los nuevos campos de modelos

### Templates base
- [x] `base.html` — Layout principal con:
  - Navbar: logo Meraki, menú de navegación, badge de notificaciones, usuario activo, logout
  - Breadcrumbs (slot via `{% block breadcrumbs %}`)
  - Área de mensajes Django (`messages`)
  - Footer
  - HTMX cargado
  - Tailwind CSS via CDN
- [x] `registration/login.html` — Página standalone de login con diseño Meraki (sin extends)
- [x] `home.html` — Dashboard con:
  - Contador de estudios por estado (tarjetas con colores)
  - Accesos rápidos: Nueva persona, Nuevo estudio, Registrar visita
  - Grid de módulos del sistema
- [x] `HomeView` en `esteconom/urls.py` con context de estadísticas (total_personas, total_estudios, estudios_en_proceso, estudios_aprobados)

### Componentes reutilizables (`templates/components/`)
- [x] `badge_estado.html` — Badge de color según estado del estudio
- [x] `badge_riesgo.html` — Badge según nivel de riesgo
- [x] `pagination.html` — Paginación Tailwind
- [x] `form_field.html` — Campo con label + error
- [x] `confirm_modal.html` — Modal de confirmación (HTMX)
- [x] `empty_state.html` — Estado vacío para listas sin resultados
- [x] `card_persona.html` — Tarjeta resumen de persona
- [x] `notif_badge.html` — Badge de notificaciones no leídas

---

## FASE 2 — Expediente del candidato (panel analista)

**Estado:** ✅ Completada
**Prioridad:** 🔴 Crítico
**Dependencias:** FASE 1

### Objetivo
Permitir al analista capturar y gestionar el expediente completo desde el sistema interno.

### Templates de `personas`
- [x] `persona_list.html` — Tabla paginada con búsqueda por folio/nombre/CURP
- [x] `persona_detail.html` — Vista hub con pestañas: Datos, Documentos, Estudios, Domicilios
- [x] `persona_form.html` — Formulario creación/edición (shared create+update)
- [x] `persona_confirm_delete.html` — Confirmación de borrado con advertencia de cascada

### Templates de `estudios`
- [x] `estudio_list.html` — Lista con filtros por estado (tabs o badges), búsqueda
- [x] `estudio_detail.html` — Vista hub con pestañas:
  - Resumen general
  - Domicilio
  - Educación / Idiomas
  - Salud
  - Familia
  - Laboral
  - Económico
  - Visitas
  - Documentos
  - Evaluación
- [x] `estudio_form.html` — Crear/editar estudio
- [x] `estudio_confirm_delete.html` — Confirmación de borrado con advertencia cascada
- [x] `estudio_estado.html` (partial) — Cambio de estado con confirmación

### Templates de datos relacionados (desde detalle del estudio/persona)
- [x] `domicilios/domicilio_form.html`
- [x] `educacion/educacion_form.html` + `idioma_form.html`
- [x] `personas/saludpersona_form.html` (modelo en app personas)
- [x] `familia/grupofamiliar_form.html`
- [x] `laboral/historiallaboral_form.html` + sección de verificación
- [x] `referencias/referencia_form.html` + sección de verificación
- [x] `economia/situacioneconomica_form.html` — con resumen dinámico en JS
- [x] `evaluacion/evaluacionriesgo_form.html` — con cálculo de score_final en JS

### Templates de `documentos`
- [x] `documento_list.html` — Bandeja de documentos con filtros por tipo y estado
- [x] `documento_form.html` — Upload con preview (FileReader API)
- [x] Botón "Marcar verificado" inline via form POST simple

### Lógica de cambio de estado
- [x] Vista `CambiarEstadoView` con validación de `TRANSICIONES_VALIDAS`
- [x] Modal de confirmación con campo de observación en `estudio_detail.html`
- [x] Botones de transición según estado actual (solo muestra los válidos)

### Actualizaciones de vistas
- [x] `PersonaListView.get_queryset()` — búsqueda por folio/nombre/CURP
- [x] `EstudioListView.get_queryset()` — búsqueda y filtro por estado
- [x] `EstudioDetailView.get_context_data()` — contexto de transiciones válidas
- [x] `DocumentoListView.get_queryset()` — filtro por tipo y estado verificado
- [x] `SaludPersonaCreateView` + `SaludPersonaUpdateView` — nuevas vistas en app personas
- [x] Rutas de Idioma agregadas a `educacion/urls.py`
- [x] Ruta `cambiar_estado` agregada a `estudios/urls.py`
- [x] Rutas de `SaludPersona` agregadas a `personas/urls.py`

*Completada el 2026-02-22.*

---

## FASE 3 — Portal público de autogestión (Escenario A)

**Estado:** ✅ Completada
**Prioridad:** 🟠 Alto
**Dependencias:** FASE 0, FASE 1

### Objetivo
Link único con token que el candidato abre desde su celular para llenar su propio estudio, sin necesidad de crear una cuenta.

### URL del portal
```
/candidato/<uuid:token>/          → página de bienvenida
/candidato/<uuid:token>/paso/<n>/ → cada paso del wizard
/candidato/<uuid:token>/gracias/  → confirmación de envío
/candidato/<uuid:token>/invalido/ → token inválido/expirado/completado
```

### Wizard multi-paso (7 pasos, mobile-first)

| Paso | Contenido | Modelo(s) |
|------|-----------|-----------|
| 1 | Datos personales e identificaciones | `Persona` |
| 2 | Domicilio y características del inmueble | `Domicilio` |
| 3 | Educación, idiomas y salud | `Educacion`, `Idioma`, `SaludPersona` |
| 4 | Grupo familiar (todos los que viven en casa) | `GrupoFamiliar` |
| 5 | Situación económica y patrimonio | `SituacionEconomica` |
| 6 | Referencias personales (mínimo 3) | `Referencia` |
| 7 | Historial laboral + subida de foto y documentos | `HistorialLaboral`, `Documento` |

### Funcionalidades del portal
- [x] Acceso sin login — validación solo por token UUID
- [x] Validación de token: expirado, ya completado, inválido
- [x] Barra de progreso visual entre pasos
- [x] Guardado automático al avanzar cada paso (el candidato puede retomar)
- [x] Upload de foto desde cámara del celular (retrato, fachada, interior)
- [x] Formularios adaptativos mobile-first (inputs grandes, teclado numérico donde aplique)
- [x] Página de confirmación al completar: mensaje de éxito + marcar `EstudioToken.activo=False`
- [ ] Notificación automática al analista cuando el candidato completa el formulario (pendiente FASE 6)

### Vista del analista para gestionar tokens
- [x] Botón "Generar link para candidato" en detalle del estudio
- [x] Mostrar link generado con botón de copiar
- [x] Indicador de estado: Pendiente / Completado / Expirado
- [x] Botón para regenerar token (invalida el anterior)

### Archivos creados en esta fase
- `apps/estudios/forms_candidato.py` — Formularios de cada paso del wizard
- `apps/estudios/views_candidato.py` — Vistas del portal + gestión de tokens del analista
- `apps/estudios/urls_candidato.py` — URLs del portal (actualizado)
- `apps/estudios/urls.py` — Rutas de generar/regenerar token añadidas
- `apps/estudios/views.py` — `EstudioDetailView` expone `token_candidato` en contexto
- `templates/candidato/base_candidato.html` — Layout mobile-first del portal
- `templates/candidato/bienvenida.html`
- `templates/candidato/token_invalido.html`
- `templates/candidato/paso_1.html` al `paso_7.html` (7 templates)
- `templates/candidato/gracias.html`
- `templates/estudios/estudio_detail.html` — Sección de token del candidato añadida

*Completada el 2026-02-22.*

---

## FASE 4 — App del inspector en campo (Escenario B)

**Estado:** ✅ Completada
**Prioridad:** 🟠 Alto
**Dependencias:** FASE 1, FASE 2

### Objetivo
Interfaz mobile-first para que el inspector registre la visita domiciliaria, capture fotos y verifique referencias por teléfono.

### Agenda del inspector
- [x] `visitas/agenda.html` — Lista de visitas asignadas al usuario actual:
  - Fecha y hora, nombre del candidato, dirección, estado
  - Ordenadas por fecha ascendente (hoy / próximas / pasadas — secciones colapsables)
  - Botón "Iniciar visita" que abre el formulario de reporte
- [x] `AgendaInspectorView` en `apps/visitas/views.py` — filtra `evaluador=request.user`
- [x] Ruta `visitas/agenda/` → `visitas:agenda_inspector`

### Formulario de reporte de visita (mobile-first)
- [x] `visitas/visitadomiciliaria_reporte_form.html` — Secciones:
  - **Ubicación:** Captura GPS automática (API Geolocation del navegador)
  - **Verificación:** ¿Se encontró a la persona? ¿El domicilio coincide?
  - **Entorno:** Botones radio 1-5 para seguridad, ruido, acceso a transporte; select tipo_zona
  - **Observaciones:** 3 textareas (observaciones, comentarios colonos, recomendación)
  - **Fotos:** Banner informativo (upload desde sección Documentos)
- [x] `VisitaDomiciliariaCreateView` y `UpdateView` usan `visitadomiciliaria_reporte_form.html`

### Upload de fotos en campo
- [ ] Captura directa desde cámara del celular (input `capture="camera"`) — pendiente FASE 5
- [ ] Guardado como `Documento` con tipo `FOT` — pendiente FASE 5

### Verificación telefónica de referencias
- [x] `VerificarReferenciaView` en `apps/referencias/views.py`
- [x] Template `referencias/referencia_verificar_form.html`:
  - Card con datos de la referencia, teléfonos tappables (`tel:`)
  - Campos de resultado: conducta, cualidades, actividad tiempo libre, lugares laborados
  - Botón "Marcar como verificada y guardar" → `verificada=True` + `fecha_verificacion`
- [x] Ruta `<pk>/verificar/` → `referencias:referencia_verificar`

### Verificación telefónica de historial laboral
- [x] `VerificarHistorialLaboralView` en `apps/laboral/views.py`
- [x] Template `laboral/historiallaboral_verificar_form.html`:
  - Card con datos del empleo, teléfonos tappables
  - Notas de verificación + botón "Marcar como verificado"
- [x] Ruta `<pk>/verificar/` → `laboral:historiallaboral_verificar`

*Completada el 2026-02-23.*

---

## FASE 5 — Generación del reporte PDF

**Estado:** ✅ Completada
**Prioridad:** 🟠 Alto
**Dependencias:** FASE 2, FASE 3 o FASE 4

### Objetivo
Generar el PDF final idéntico al formato de referencia de Meraki.

### Stack técnico
- **Librería:** `WeasyPrint` (renderiza HTML+CSS a PDF, soporta imágenes y tablas complejas)
- **Mapa:** OpenStreetMap Static Maps API (gratuito, sin API key) via `staticmap.openstreetmap.de`
- **Instalación:** `weasyprint` agregado a `requirements.txt`

### Estructura del template HTML del reporte
```
templates/reportes/
├── estudio_pdf.html        ← template principal con CSS A4 optimizado para WeasyPrint
├── _pdf_header.html        ← encabezado reutilizable: logo empresa + folio + estado
├── _pdf_portada.html       ← foto candidato + score + comentarios y conclusiones
├── _pdf_datos_personales.html  ← datos personales + identificaciones + educación + idiomas
├── _pdf_salud_familia.html     ← salud + historial laboral + grupo familiar
├── _pdf_inmueble_economia.html ← inmueble + servicios/materiales + ingresos/egresos + créditos
├── _pdf_referencias.html       ← referencias + verificaciones + observaciones de colonos
├── _pdf_croquis.html           ← mapa estático GPS + tabla de entorno
└── _pdf_fotos.html             ← galería de fotos en tabla 2 columnas (WeasyPrint-compatible)
```

### Vista de generación
- [x] `GenerarReportePDFView` en `apps/reportes/views.py` — genera y descarga PDF
- [x] `VistaPreviewReporteView` — renderiza HTML para vista previa en nueva pestaña
- [x] Botón "Vista previa" + "Descargar PDF" en estudio_detail.html (estados COM/REV/APR/REC)
- [x] Botón deshabilitado (con tooltip) en otros estados
- [x] Descarga directa como `Estudio_<folio>_<fecha>.pdf`
- [x] Rutas registradas en `esteconom/urls.py` → `apps/reportes/urls.py`

### Tareas técnicas
- [x] `weasyprint` agregado a `requirements.txt`
- [x] CSS puro para impresión A4 (`@page { size: A4; margin: 1.5cm 1.8cm; }`)
- [x] Mapa estático OpenStreetMap desde coordenadas GPS de `VisitaDomiciliaria`
- [x] Aspectos positivos/negativos, conclusión y recomendación final en portada
- [x] Logo de `EmpresaCliente` en encabezado (con fallback a texto)
- [x] Todos los campos opcionales con fallback `default:"N/A"`

*Completada el 2026-02-23.*

---

## FASE 6 — Notificaciones y flujo automatizado

**Estado:** ✅ Completada (parcial — ver pendientes)
**Prioridad:** 🟡 Medio
**Dependencias:** FASE 2

### Objetivo
Automatizar las notificaciones internas y el flujo de estados del estudio.

### Tareas
- [ ] Implementar `transicionar(nuevo_estado, usuario)` en `EstudioSocioeconomico` con validación de `TRANSICIONES_VALIDAS` *(la validación existe en `CambiarEstadoView`; el método formal en el modelo queda pendiente)*
- [x] `pre_save` + `post_save` signal en `EstudioSocioeconomico` → crear `Notificacion` al cambiar estado (`apps/notificaciones/signals.py`)
- [ ] `post_save` signal → notificar al analista cuando el candidato completa el portal *(pendiente — Fase 3 completada sin este hook)*
- [x] Templates de `notificaciones`: `notificacion_list.html` (paginada, marcar leída con HTMX), `notificacion_detail.html`
- [x] Badge dinámico en navbar (HTMX polling cada 30 segundos via `NotifCountView`)
- [x] Configuración de email vía `.env` (`EMAIL_HOST`, `EMAIL_HOST_USER`, etc.) — `console.EmailBackend` por defecto; envío real pendiente de integración con proveedor SMTP
- [x] `MarcarLeidaView` y `MarcarTodasLeidasView` con soporte HTMX
- [x] Context processor `notif_count` → `notif_count_global` disponible en todos los templates

*Completada parcialmente el 2026-02-24.*

---

## FASE 7 — Roles y control de acceso

**Estado:** ✅ Completada (parcial — ver pendientes)
**Prioridad:** 🟡 Medio
**Dependencias:** FASE 2

### Objetivo
Diferenciar el acceso y las funcionalidades según el rol del usuario en el sistema.

### Roles del sistema

| Código | Rol | Acceso |
|--------|-----|--------|
| `ANA` | Analista | Panel completo, generación de PDF, aprobación/rechazo |
| `INS` | Inspector | Solo agenda de visitas + app de campo |

> El **candidato** no tiene cuenta en el sistema — accede solo via token público.

### Modelo `PerfilUsuario` implementado
```python
# apps/usuarios/models.py
class PerfilUsuario(models.Model):
    usuario = OneToOneField(User, CASCADE, related_name='perfil')
    ROL = [('ANA', 'Analista'), ('INS', 'Inspector')]
    rol = CharField(max_length=3, choices=ROL, default='ANA')
    telefono = CharField(max_length=15, blank=True)
    activo = BooleanField(default=True)
    # Nota: campo `foto` del plan original no implementado (simplificado a `telefono`)
```

### Tareas
- [x] Crear modelo `PerfilUsuario` en nueva app `apps/usuarios/` con campos `rol`, `telefono`, `activo`
- [x] Crear `RolRequeridoMixin`, `AnalistaRequeridoMixin`, `InspectorRequeridoMixin` en `apps/usuarios/mixins.py`
- [ ] Redireccionamiento post-login: `ANA` → dashboard, `INS` → agenda *(pendiente — actualmente ambos van a `/`)*
- [x] Admin inline en User + admin propio de `PerfilUsuario` (`apps/usuarios/admin.py`)
- [x] Señal `post_save` en `User` para crear `PerfilUsuario` automáticamente (`apps/usuarios/signals.py`)
- [x] Context processor `perfil_usuario` → `es_analista`, `es_inspector` disponibles en todos los templates
- [x] Navbar adaptativo: "Evaluaciones" y "Usuarios" solo visibles para analistas
- [x] Vistas: `MiPerfilView`, `MiPerfilEditarView`, `UsuarioListView`, `UsuarioRolEditarView`
- [x] Templates: `mi_perfil.html`, `perfil_form.html`, `usuario_list.html`

*Completada parcialmente el 2026-02-24.*

---

## Dependencias técnicas adicionales a instalar

```bash
pip install weasyprint        # Generación de PDF desde HTML
pip install Pillow            # Manejo de imágenes (ya instalado)
pip install django-crispy-forms tailwind  # Formularios con Tailwind (opcional)
```

Agregar al `requirements.txt`:
```
weasyprint
Pillow
```

---

## Resumen del estado del plan

| Fase | Nombre | Prioridad | Estado |
|------|--------|-----------|--------|
| 0 | Completar modelos | 🔴 Crítico | ✅ Completada |
| 1 | Base de templates y auth | 🔴 Crítico | ✅ Completada |
| 2 | Expediente del candidato (analista) | 🔴 Crítico | ✅ Completada |
| 3 | Portal público de autogestión | 🟠 Alto | ✅ Completada |
| 4 | App del inspector en campo | 🟠 Alto | ✅ Completada |
| 5 | Generación del reporte PDF | 🟠 Alto | ✅ Completada |
| 6 | Notificaciones y flujo automatizado | 🟡 Medio | ✅ Completada (parcial) |
| 7 | Roles y control de acceso | 🟡 Medio | ✅ Completada (parcial) |

### Pendientes restantes de Fase 6 y 7

| # | Tarea | Fase |
|---|-------|------|
| A | Método formal `transicionar()` en modelo `EstudioSocioeconomico` | 6 |
| B | Signal al completar portal del candidato (Fase 3) → notificar analista | 6 |
| C | Envío real de email SMTP en APR/REC (configurar proveedor) | 6 |
| D | Redirección post-login por rol: `ANA` → `/`, `INS` → `/visitas/agenda/` | 7 |
| E | Campo `foto` en `PerfilUsuario` (simplificado en esta implementación) | 7 |

---

*Plan elaborado el 2026-02-21. Actualizado el 2026-02-24 tras completar Fase 6 (notificaciones automáticas) y Fase 7 (sistema de roles PerfilUsuario).*
*Basado en el reporte PDF de referencia (Meraki Consultoría) y el análisis del formulario Google Forms de Meraki.*
