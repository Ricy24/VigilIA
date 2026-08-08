# TASKS.md — Tareas Activas

Última actualización: 2026-08-08
Fase actual: **Fase 2 — Vision Pipeline**

---

## 🔄 En Progreso — Fase 2: Vision Pipeline

- [ ] Wrapper Ultralytics YOLOv11 (`detection/`)
- [ ] Wrapper ByteTrack (`tracking/`)
- [ ] Ingesta RTSP (`ingestion/`)
- [ ] Procesador de video principal
- [ ] Test unitarios / de integración pipeline

---

## Completadas en Fase 0

- [x] Crear estructura de directorios completa
- [x] `backend/requirements.txt` con deps pinneadas
- [x] `inference/requirements.txt` con deps pinneadas
- [x] `backend/app/main.py` — FastAPI app base
- [x] `backend/app/core/config.py` — pydantic-settings
- [x] `backend/app/api/v1/router.py`
- [x] `backend/app/api/v1/endpoints/health.py`
- [x] `backend/app/db/session.py`
- [x] `backend/app/db/base.py`
- [x] `backend/Dockerfile` multi-stage
- [x] `inference/pipeline/config.py`
- [x] `inference/pipeline/main.py`
- [x] `inference/Dockerfile` multi-stage
- [x] `frontend/package.json`
- [x] `frontend/vite.config.ts`
- [x] `frontend/tsconfig.json`
- [x] `frontend/index.html`
- [x] `frontend/src/index.css` — design system
- [x] `frontend/src/App.tsx`
- [x] `frontend/src/App.css`
- [x] `frontend/Dockerfile` multi-stage
- [x] `docker/docker-compose.dev.yml`
- [x] `docker/.env.example`
- [x] `.gitignore` actualizado
- [x] Todos los `__init__.py` de packages Python
- [x] Todos los archivos `Ai/` actualizados

---

## ✅ Fase 0 — Verificación Completada

- [x] `.venv` backend instalado (41 paquetes) — FastAPI carga OK
- [x] `.venv` inference creado
- [x] `npm install` frontend (226 paquetes) — TypeScript sin errores
- [x] Docker Compose configurado (levanta cuando Docker Desktop está activo)

---

## ✅ Fase 1 — Backend Core Completada

- [x] Setup Alembic en backend
- [x] Modelo ORM: User, Camera, Zone, Event, Alert
- [x] Migración inicial de Alembic (realizada exitosamente en Postgres)
- [x] Autenticación JWT y roles
- [x] Endpoints CRUD de cámaras y zonas funcionales y probados.

---

## Backlog — Fases 2-7

Ver `Ai/ROADMAP.md` para el detalle de cada fase.
