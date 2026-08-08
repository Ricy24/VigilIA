# TASKS.md — Tareas Activas

Última actualización: 2026-08-08
Fase actual: **Fase 0 — Fundación**

---

## En Progreso

- [/] **Fase 0: Verificación final** — crear virtualenvs, instalar deps, verificar Docker

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

## Pendiente — Fase 0 (verificación)

- [ ] Crear `.venv` en `backend/` e instalar requirements
- [ ] Crear `.venv` en `inference/` e instalar requirements
- [ ] `npm install` en `frontend/`
- [ ] `docker compose up postgres redis` — verificar que levanta

---

## Backlog — Fase 1 (próxima)

- [ ] Setup Alembic en backend
- [ ] Modelo ORM: User
- [ ] Modelo ORM: Camera
- [ ] Modelo ORM: Zone
- [ ] Modelo ORM: Event
- [ ] Modelo ORM: Alert
- [ ] Migración inicial de Alembic
- [ ] Endpoint: POST /auth/login (JWT)
- [ ] Endpoint: POST /auth/refresh
- [ ] Endpoint: GET /auth/me
- [ ] CRUD completo: /cameras
- [ ] CRUD completo: /zones
- [ ] Tests unitarios de endpoints
- [ ] Actualizar Ai/TASKS.md y Ai/ROADMAP.md

---

## Backlog — Fases 2-7

Ver `Ai/ROADMAP.md` para el detalle de cada fase.
