# Plan Final de Implementación — EstudioEcoNom

**Versión:** 1.0
**Fecha:** 2026-04-27
**Estado del proyecto:** Fases 1–9 completadas

---

## Discrepancia Documentada

### `apps/reportes/views.py` — Nombres de funciones auxiliares

CONTEXT.md sección 2.14 documenta `_construir_mapa_url` pero el nombre real en el código es distinto.
La función fue refactorizada en algún momento sin actualizar la documentación.

| CONTEXT.md dice | Código real | Descripción real |
|-----------------|-------------|------------------|
| `_construir_mapa_url(lat, lon)` | `_url_mapa(lat, lon)` | Construye la URL del mapa estático con prioridad Google Maps → Mapbox → OpenStreetMap. Retorna una tupla `(url, proveedor)`. |
| *(no documentada)* | `_descargar_imagen_mapa(lat, lon)` | Descarga el mapa estático y lo retorna como data URL en base64 para que WeasyPrint no haga peticiones externas al renderizar el PDF. Retorna `None` si falla la descarga. |

**Acción requerida en CONTEXT.md:** Actualizar sección 2.14 con los nombres correctos y agregar `_descargar_imagen_mapa`.

---

## Integraciones Pendientes

---

### Tarea 21 — `apps/auditorias` — Registro de auditoría

**Estado:** App creada, `models.py` vacío, sin `urls.py`.
**Impacto:** Trazabilidad completa de acciones en el sistema.

**Objetivo:**
Registrar automáticamente quién modificó qué y cuándo en los modelos principales, sin intervención manual en las vistas.

**Plan de implementación:**

#### Paso 1 — Modelo `RegistroAuditoria`
```python
# apps/auditorias/models.py
class RegistroAuditoria(models.Model):
    usuario       = FK → auth.User, SET_NULL, null
    accion        = choices: CRE/MOD/ELI/CAM  (Creó, Modificó, Eliminó, Cambió estado)
    modelo        = CharField(100)             # Ej: "EstudioSocioeconomico"
    objeto_id     = PositiveIntegerField()     # PK del objeto afectado
    descripcion   = TextField()               # Mensaje legible: "Cambió estado BOR → VIS"
    datos_antes   = JSONField(null=True)       # Snapshot antes del cambio
    datos_despues = JSONField(null=True)       # Snapshot después del cambio
    ip_address    = GenericIPAddressField(null=True)
    created_at    = DateTimeField(auto_now_add=True)
```

#### Paso 2 — Signals
Conectar `post_save` y `post_delete` en los modelos críticos:
- `EstudioSocioeconomico` — registrar cambios de estado y modificaciones
- `Persona` — registrar creación y modificaciones
- `EvaluacionRiesgo` — registrar creación y modificaciones
- `Documento` — registrar verificaciones
- `HistorialLaboral` / `Referencia` — registrar verificaciones

#### Paso 3 — Middleware para capturar IP y usuario
Crear `apps/auditorias/middleware.py` que almacene `request.user` y la IP en un thread-local para que los signals lo puedan acceder.

#### Paso 4 — Vistas de consulta (solo lectura)
- `AuditoriaListView` — lista paginada con filtros por modelo, usuario, rango de fechas
- No requiere Create/Update/Delete — solo lectura

#### Paso 5 — Registrar en `esteconom/urls.py`
```python
path('auditorias/', include('apps.auditorias.urls')),
```

**Archivos a crear/modificar:**
- `apps/auditorias/models.py`
- `apps/auditorias/signals.py`
- `apps/auditorias/middleware.py`
- `apps/auditorias/admin.py`
- `apps/auditorias/views.py`
- `apps/auditorias/urls.py`
- `templates/auditorias/auditoria_list.html`
- `esteconom/settings.py` — agregar middleware de auditoría
- `esteconom/urls.py` — agregar ruta

---

### Tarea 22 — `apps/api` — Endpoints REST con Django REST Framework

**Estado:** App creada, `models.py` vacío, sin `urls.py`.
**Impacto:** Permite integraciones externas y futuro frontend desacoplado.

**Objetivo:**
Exponer los recursos principales del sistema como API REST con autenticación por token.

**Dependencias a instalar:**
```
djangorestframework
djangorestframework-simplejwt   # Autenticación JWT
django-filter                   # Filtros en querysets
```

**Plan de implementación:**

#### Paso 1 — Configuración base
```python
# settings.py
INSTALLED_APPS += ['rest_framework', 'rest_framework_simplejwt', 'django_filters']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```

#### Paso 2 — Serializers prioritarios
```
apps/api/serializers.py
  PersonaSerializer          — campos de Persona (folio, nombre, email)
  EstudioSerializer          — campos de EstudioSocioeconomico + estado
  EstudioDetalleSerializer   — estudio completo con relaciones anidadas
  EvaluacionRiesgoSerializer — puntuaciones y análisis
```

#### Paso 3 — ViewSets
```
apps/api/views.py
  PersonaViewSet          — list, retrieve (solo lectura para externos)
  EstudioViewSet          — list, retrieve, update (cambio de estado)
  EvaluacionRiesgoViewSet — list, create, retrieve, update
```

#### Paso 4 — URLs
```python
# apps/api/urls.py
router = DefaultRouter()
router.register('personas', PersonaViewSet)
router.register('estudios', EstudioViewSet)
router.register('evaluaciones', EvaluacionRiesgoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
```

#### Paso 5 — Registrar en `esteconom/urls.py`
```python
path('api/v1/', include('apps.api.urls')),
```

**Archivos a crear/modificar:**
- `apps/api/serializers.py`
- `apps/api/views.py`
- `apps/api/urls.py`
- `apps/api/permissions.py` — permisos basados en rol (`PerfilUsuario`)
- `esteconom/settings.py`
- `esteconom/urls.py`
- `requirements.txt`

---

### Tarea 23 — Tests automatizados

**Estado:** Sin tests implementados. Solo placeholders vacíos.
**Impacto:** Calidad, regresiones, confianza para deploys.

**Objetivo:**
Suite mínima que cubra los flujos críticos del sistema.

**Plan de implementación:**

#### Prioridad 1 — Tests de modelos
```
apps/personas/tests.py
  - TestPersonaFolio: generación de folio YYYYMMNNNNN
  - TestPersonaFolioUnico: dos personas en el mismo mes → folios distintos

apps/estudios/tests.py
  - TestTransicionesEstado: TRANSICIONES_VALIDAS respetadas
  - TestCambiarEstadoView: POST con estado inválido → 400

apps/economia/tests.py
  - TestSituacionEconomicaProperties: ingreso_total, egreso_total, capacidad_ahorro
```

#### Prioridad 2 — Tests de vistas
```
apps/estudios/tests.py
  - TestEstudioDetailView: requiere login, muestra datos correctos
  - TestCambiarEstadoView: transición válida guarda nuevo estado

apps/estudios/tests_ia.py
  - TestAnalizarEstudioIAView: mock de anthropic.Anthropic, verifica guardado en BD
  - TestSugerirEvaluacionIAView: mock de anthropic.Anthropic, verifica respuesta JSON

apps/candidato/tests.py (en apps/estudios/)
  - TestPortalCandidato: token válido → acceso, token inválido → redirección
```

#### Prioridad 3 — Tests de integración
```
  - TestFlujoCandidatoCompleto: token → pasos 1-7 → gracias → token desactivado
  - TestGenerarReportePDF: estudio en estado COM → respuesta 200 con Content-Type PDF
```

**Comando para correr tests:**
```bash
python manage.py test apps.personas apps.estudios apps.economia --verbosity=2
```

**Archivos a crear:**
- `apps/personas/tests.py`
- `apps/estudios/tests.py`
- `apps/estudios/tests_ia.py`
- `apps/economia/tests.py`

---

### Tarea 24 — Race condition en folio de `Persona`

**Estado:** El método `Persona.save()` genera el folio sin transacción atómica.
**Impacto:** En producción con carga concurrente puede generar folios duplicados.

**Código actual (problemático):**
```python
# apps/personas/models.py — save()
last = Persona.objects.filter(
    folio__startswith=f'{year}{month}'
).order_by('-folio').first()
# ← VENTANA DE RACE CONDITION AQUÍ
# Si dos requests llegan simultáneamente, ambos pueden obtener el mismo `last`
# y generar el mismo folio siguiente
```

**Plan de implementación:**

#### Fix recomendado — `select_for_update()` dentro de transacción atómica
```python
# apps/personas/models.py
from django.db import transaction

def save(self, *args, **kwargs):
    if not self.folio:
        with transaction.atomic():
            year = timezone.now().strftime('%Y')
            month = timezone.now().strftime('%m')
            last = (
                Persona.objects
                .select_for_update()
                .filter(folio__startswith=f'{year}{month}')
                .order_by('-folio')
                .first()
            )
            if last:
                ultimo_num = int(last.folio[6:])
                self.folio = f'{year}{month}{str(ultimo_num + 1).zfill(5)}'
            else:
                self.folio = f'{year}{month}00001'
    super().save(*args, **kwargs)
```

**Nota:** `select_for_update()` solo funciona con PostgreSQL o MySQL en producción. Con SQLite (desarrollo) no bloquea filas pero tampoco hay riesgo real de concurrencia.

**Archivos a modificar:**
- `apps/personas/models.py` — método `save()`
- `apps/personas/tests.py` — test de concurrencia con `ThreadPoolExecutor`

---

## Resumen de Prioridades

| # | Tarea | Esfuerzo estimado | Prioridad |
|---|-------|-------------------|-----------|
| 24 | Race condition folio | Bajo — 1 archivo, 10 líneas | Alta — afecta integridad de datos |
| 21 | Auditorías | Medio — 7 archivos nuevos | Media — trazabilidad |
| 23 | Tests | Medio — 4 archivos nuevos | Media — calidad |
| 22 | API REST | Alto — 5 archivos + deps | Baja — para integraciones futuras |

---

## Orden de Ejecución Sugerido

```
1. Tarea 24 (folio)     ← fix puntual, sin dependencias
2. Tarea 21 (auditorias) ← base para trazabilidad antes de API
3. Tarea 23 (tests)      ← validar lo ya implementado + lo nuevo
4. Tarea 22 (API REST)   ← cuando se necesiten integraciones externas
```

---

*Documento generado el 2026-04-27. Actualizar cuando se complete cada tarea.*
