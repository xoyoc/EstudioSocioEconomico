# EstudioEcoNom — Sistema de Gestión de Estudios Socioeconómicos

Sistema web para digitalizar y gestionar el proceso de estudios socioeconómicos de **Meraki Consultoría**. Permite capturar el expediente completo de un candidato, coordinar visitas domiciliarias, verificar referencias y generar el reporte PDF final.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Django 6.0.2 · Python 3.12 |
| Base de datos | SQLite (desarrollo) · PostgreSQL (producción) |
| Frontend | Tailwind CSS v3 (CDN) · HTMX 1.9.12 |
| Reportes PDF | WeasyPrint 68.1 |
| Configuración | `python-decouple` · `dj-database-url` |
| Imágenes | Pillow 12.1 |
| Idioma / TZ | `es-mx` · `America/Mexico_City` |

---

## Requisitos previos

- Python 3.12+
- Git
- (Opcional) PostgreSQL si no se usa SQLite
- Dependencias de sistema para WeasyPrint ([ver docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html))

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd EstudioSocioEconomico
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venvEstudioEcoNom
source .venvEstudioEcoNom/bin/activate   # Linux / macOS
.venvEstudioEcoNom\Scripts\activate      # Windows
```

### 3. Instalar dependencias

```bash
pip install django==6.0.2 python-decouple dj-database-url psycopg2-binary Pillow weasyprint
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=cambia-esta-clave-por-una-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Opcional — si no se define, usa SQLite
# DATABASE_URL=postgres://usuario:password@localhost:5432/estudioeconom

# Email — consola por defecto; configurar para producción
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.ejemplo.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=correo@ejemplo.com
# EMAIL_HOST_PASSWORD=contraseña
# DEFAULT_FROM_EMAIL=noreply@meraki-consultoria.mx
```

### 5. Aplicar migraciones y crear superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

Accede en: [http://localhost:8000](http://localhost:8000)
Panel de administración: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Comandos de desarrollo

```bash
# Activar el entorno virtual
source .venvEstudioEcoNom/bin/activate

# Servidor de desarrollo
python manage.py runserver

# Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Ejecutar todos los tests
python manage.py test

# Tests de una app específica
python manage.py test apps.personas
python manage.py test apps.estudios.tests.TestClassName.test_method

# Shell de Django
python manage.py shell

# Recolectar archivos estáticos (producción)
python manage.py collectstatic
```

---

## Estructura del proyecto

```
EstudioSocioEconomico/
├── esteconom/              # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py             # Enrutador principal
│   └── wsgi.py / asgi.py
│
├── apps/                   # 16 apps de dominio
│   ├── configuracion/      # TimestampModel base + catálogos (TipoEstudio, EmpresaCliente)
│   ├── personas/           # Entidad central: Persona + SaludPersona
│   ├── estudios/           # Nodo hub: EstudioSocioeconomico (máquina de estados) + EstudioToken
│   ├── domicilios/         # Dirección y características de vivienda
│   ├── economia/           # Situación económica (ingresos, egresos, patrimonio)
│   ├── educacion/          # Historial educativo + idiomas + niveles
│   ├── laboral/            # Historial laboral con flujo de verificación
│   ├── familia/            # Grupo familiar y dependencia económica
│   ├── referencias/        # Referencias personales con verificación
│   ├── visitas/            # Visitas domiciliarias con GPS + agenda del inspector
│   ├── evaluacion/         # Scoring de riesgo (6 categorías)
│   ├── documentos/         # Gestión documental con verificación y subida de archivos
│   ├── notificaciones/     # Notificaciones automáticas por cambio de estado (signals)
│   ├── usuarios/           # Perfiles con roles (Analista/Inspector) + mixins de acceso
│   ├── reportes/           # Generación de PDF con WeasyPrint + vista previa HTML
│   ├── auditorias/         # Pendiente — log de cambios
│   └── api/                # Pendiente — endpoints REST
│
├── templates/              # 90+ templates HTML
│   ├── base.html           # Layout principal con Tailwind CSS + navbar
│   ├── home.html           # Dashboard con estadísticas y accesos rápidos
│   ├── registration/       # Login / logout
│   ├── candidato/          # Portal público de autogestión (7 pasos)
│   ├── components/         # 8 componentes reutilizables (badges, modals, paginación)
│   ├── reportes/           # Templates PDF (portada, datos, croquis, fotos, etc.)
│   └── <app_name>/         # Templates CRUD por módulo
│
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos por usuarios (creado automáticamente)
├── implementacion/         # Plan de implementación por fases
├── CONTEXT.md              # Documentación técnica completa de la arquitectura
├── AGENTS.md               # Guía para agentes de IA (Warp/Oz)
└── manage.py
```

---

## Flujo de estados del estudio

```
BOR (Borrador) → VIS (Visita programada) → PRO (En proceso)
                                               ↓
                                          COM (Completado)
                                               ↓
                                          REV (En revisión)
                                          ↙           ↘
                                    APR (Aprobado)  REC (Rechazado)
                                                         ↓
                                                    BOR (reabrir)

Desde BOR, VIS, PRO → CAN (Cancelado)
```

Las transiciones están validadas en `apps/estudios/views.py` (`TRANSICIONES_VALIDAS`). Cada cambio de estado dispara notificaciones automáticas vía signals (`apps/notificaciones/signals.py`).

---

## Escenarios de operación

**Escenario A — Autogestión del candidato**
1. El analista crea el estudio y genera un link con token UUID único (expiración 30 días)
2. El candidato accede al portal público desde su celular (sin cuenta)
3. Completa 7 pasos: datos personales → domicilio → educación/salud → familia → economía → referencias (mín. 3) → empleo y documentos
4. Al finalizar, el token se desactiva y el estudio avanza a estado `PRO`
5. El analista revisa, complementa, evalúa riesgo y genera el PDF

**Escenario B — Inspector en campo**
1. El analista crea el estudio y agenda una visita domiciliaria
2. El inspector consulta su agenda (`/visitas/agenda/`) con visitas de hoy, próximas y pasadas
3. Captura coordenadas GPS, evalúa zona (seguridad, ruido, transporte) y registra observaciones
4. Verifica referencias y empleo por teléfono (campos `verificado` + `fecha_verificacion`)
5. El analista revisa y genera el PDF

---

## Roles del sistema

| Rol | Acceso | Implementación |
|---|---|---|
| **Analista** (`ANA`) | Panel completo, gestión de estudios, aprobación/rechazo, generación de PDF, administración de usuarios | `AnalistaRequeridoMixin` |
| **Inspector** (`INS`) | Agenda de visitas, captura en campo, verificación de referencias y empleo | `InspectorRequeridoMixin` |
| **Candidato** | Acceso exclusivo por token UUID público, sin cuenta en el sistema | `EstudioToken` |

Los mixins de acceso están en `apps/usuarios/mixins.py`. Los superusuarios tienen acceso completo sin restricciones.

---

## Módulos principales

| URL | Módulo | Descripción |
|---|---|---|
| `/` | Dashboard | Estadísticas, accesos rápidos y navegación a módulos |
| `/personas/` | Personas | CRUD de candidatos con búsqueda (folio, nombre, CURP) |
| `/estudios/` | Estudios | Gestión de estudios socioeconómicos con filtro por estado |
| `/domicilios/` | Domicilios | Dirección y características de vivienda |
| `/laboral/` | Historial laboral | Empleos con flujo de verificación |
| `/educacion/` | Educación | Niveles educativos, idiomas y catálogo de niveles |
| `/familia/` | Familia | Grupo familiar y dependientes |
| `/referencias/` | Referencias | Referencias personales con verificación |
| `/economia/` | Economía | Situación económica (ingresos, egresos, patrimonio) |
| `/visitas/` | Visitas | Visitas domiciliarias con GPS |
| `/visitas/agenda/` | Agenda | Agenda personal del inspector (hoy/próximas/pasadas) |
| `/evaluacion/` | Evaluación | Scoring de riesgo (6 categorías + score final) |
| `/documentos/` | Documentos | Gestión documental y subida de archivos |
| `/notificaciones/` | Notificaciones | Bandeja de notificaciones con marcar leída/todas |
| `/reportes/<pk>/preview/` | Reportes | Vista previa HTML del estudio |
| `/reportes/<pk>/pdf/` | Reportes | Descarga PDF del estudio (WeasyPrint) |
| `/candidato/<uuid>/` | Portal candidato | Wizard público de 7 pasos |
| `/usuarios/` | Usuarios | Gestión de perfiles y roles (solo analistas) |
| `/admin/` | Administración | Panel de administración Django |

---

## Estado de implementación

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Modelos de base de datos (14 entidades + catálogos) | ✅ Completada |
| 1 | Templates base, autenticación y dashboard | ✅ Completada |
| 2 | Expediente del candidato — panel del analista (CRUD completo) | ✅ Completada |
| 3 | Portal público de autogestión — wizard 7 pasos con tokens UUID | ✅ Completada |
| 4 | App del inspector — agenda de visitas y captura en campo | ✅ Completada |
| 5 | Generación del reporte PDF — WeasyPrint + vista previa HTML | ✅ Completada |
| 6 | Notificaciones automáticas por cambio de estado (signals + HTMX) | ✅ Completada |
| 7 | Roles y control de acceso (Analista/Inspector/Candidato) | ✅ Completada |
| — | REST API (`apps/api`) | ⬜ Pendiente |
| — | Auditorías / log de cambios (`apps/auditorias`) | ⬜ Pendiente |
| — | Tests unitarios y de integración | ⬜ Pendiente |

### Estadísticas del código

- **~6,000 líneas** Python (sin migraciones)
- **~17,000 líneas** HTML (90+ templates)
- **~23,000 líneas** totales
- **16 apps** Django · **14 modelos** de dominio · **8 formularios** · **8 componentes** reutilizables

---

## Documentación adicional

- [`CONTEXT.md`](./CONTEXT.md) — Arquitectura detallada, modelos, relaciones y guía técnica
- [`AGENTS.md`](./AGENTS.md) — Guía para agentes de IA (Warp/Oz)
- [`implementacion/01_plan_de_implementacion.md`](./implementacion/01_plan_de_implementacion.md) — Plan de implementación por fases con checklist de tareas

---

## Contribución

Este proyecto sigue las convenciones definidas en `AGENTS.md` y `CONTEXT.md`:

- Todo el código y textos de UI en **español mexicano**
- Modelos de dominio heredan de `TimestampModel` (campos `created_by` / `updated_by`)
- Vistas internas protegidas con `LoginRequiredMixin`; acceso por rol con `AnalistaRequeridoMixin` / `InspectorRequeridoMixin`
- Campos `choices` de 3 caracteres en mayúsculas (p. ej. `'BOR'`, `'APR'`)
- Nunca asignar `Persona.folio` manualmente — se autogenera en `save()`
- Siempre poblar `created_by` y `updated_by` en `form_valid()`
- Convención de URLs: `<modelo>_list`, `<modelo>_create`, `<modelo>_detail`, `<modelo>_update`, `<modelo>_delete`
- Templates extienden `base.html` y usan Tailwind CSS vía CDN
