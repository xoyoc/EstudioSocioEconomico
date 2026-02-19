# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0.2 application for managing socioeconomic studies (estudios socioeconómicos). Tracks persons, their financial situation, employment history, education, family, references, home visits, risk evaluations, and document verification. All UI text and model fields are in Mexican Spanish (`es-mx`, timezone `America/Mexico_City`).

## Development Commands

```bash
# Activate virtual environment
source .venvEstudioEcoNom/bin/activate

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.personas
python manage.py test apps.estudios.tests.TestClassName.test_method_name

# Django shell
python manage.py shell

# Create admin user
python manage.py createsuperuser
```

## Architecture

### Django Project Layout

- `esteconom/` — Project configuration (settings, urls, wsgi/asgi)
- `apps/` — 16 domain-specific Django apps
- `templates/` — HTML templates (not yet populated)

### App Domain Map

| App | Purpose |
|-----|---------|
| `personas` | Central entity — person/applicant profiles with auto-generated folio (YYYYMMNNNNN) |
| `estudios` | Socioeconomic study records with 8-state workflow |
| `domicilios` | Address/housing info with service tracking |
| `economia` | Income, expenses, assets, debts (one-to-one with study) |
| `educacion` | Education records with level catalog |
| `laboral` | Employment history with verification workflow |
| `familia` | Family group members and dependency tracking |
| `referencias` | Personal/professional references with verification |
| `visitas` | Home visit records with GPS and neighborhood assessment |
| `evaluacion` | Risk scoring across 6 categories (one-to-one with study) |
| `documentos` | Document uploads with verification workflow |
| `notificaciones` | System notifications with priority and read tracking |
| `configuracion` | Base abstract model (`TimestampModel`) and study type catalog |
| `auditorias` | Audit logging (placeholder) |
| `reportes` | Report generation (placeholder) |
| `api` | REST API endpoints (placeholder) |

### Key Patterns

**TimestampModel** (`apps/configuracion/models.py`): Abstract base inherited by nearly all models. Provides `created_at`, `updated_at`, `created_by`, `updated_by` fields. Always populate the `_by` fields when creating/updating records.

**Central entity is `Persona`**: Most domain models relate back to `Persona` or `EstudioSocioeconomico` via ForeignKey.

**EstudioSocioeconomico state machine**: Borrador → Visita Programada → En Proceso → Completado → En Revisión → Aprobado/Rechazado/Cancelado.

**Computed properties in `SituacionEconomica`**: `ingreso_total`, `egreso_total`, `capacidad_ahorro` are model properties that calculate from stored fields.

**Verification workflows**: `HistorialLaboral`, `Referencia`, and `Documento` all have `verificado/verificada` boolean flags with associated timestamps.

### Configuration

Environment variables managed via `python-decouple` from `.env` file:
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`
- SQLite used by default; PostgreSQL (`psycopg2-binary`) when `DATABASE_URL` is set

### Current Status

Models are fully designed. Views, URL routing, admin customizations, templates, API, and tests are mostly placeholder/empty — ready for implementation.
