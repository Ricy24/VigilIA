# ROADMAP.md — Hoja de Ruta de VigilIA

Última actualización: 2026-08-08
Estado actual: **Fase 0 — En ejecución**

---

## Resumen de Fases

| Fase | Nombre | Estado | Descripción |
|------|--------|--------|-------------|
| 0 | Fundación | 🔄 En progreso | Estructura, entornos, Docker Compose, Ai/ docs |
| 1 | Backend Core | ⏳ Pendiente | Auth JWT, CRUD cameras/zones/users, DB migrations |
| 2 | Vision Pipeline | ⏳ Pendiente | RTSP ingesta, detección YOLO, tracking ByteTrack |
| 3 | Motor de Reglas SST | ⏳ Pendiente | EPP, zonas de exclusión, detección de caídas |
| 4 | Alertas WebSocket | ⏳ Pendiente | Push de alertas en tiempo real, notificaciones |
| 5 | Frontend Dashboard | ⏳ Pendiente | React, visualización cámaras, alertas, historial |
| 6 | LLM Reports | ⏳ Pendiente | Reportes narrativos de turno asistidos por LLM |
| 7 | Hardening | ⏳ Pendiente | Observabilidad, reconexión, métricas, prod Compose |

---

## Fase 0 — Fundación del Proyecto

**Objetivo:** Sentar las bases del proyecto con toda la infraestructura de desarrollo correctamente configurada.

### Entregables

- [x] Estructura completa de directorios (backend, inference, frontend, docker, scripts, tests)
- [x] `backend/requirements.txt` con dependencias pinneadas
- [x] `inference/requirements.txt` con dependencias pinneadas
- [x] `backend/app/main.py` — FastAPI base con lifespan y CORS
- [x] `backend/app/core/config.py` — Settings con pydantic-settings
- [x] `backend/app/api/v1/router.py` — Router principal
- [x] `backend/app/api/v1/endpoints/health.py` — Health check básico y completo
- [x] `backend/app/db/session.py` — Engine SQLAlchemy y get_db()
- [x] `backend/app/db/base.py` — Base declarativa ORM
- [x] `backend/Dockerfile` — Multi-stage (dev + prod)
- [x] `inference/pipeline/config.py` — Settings del pipeline
- [x] `inference/pipeline/main.py` — Entry point del pipeline
- [x] `inference/Dockerfile` — Multi-stage
- [x] `frontend/package.json` — React + Vite + TS + dependencias
- [x] `frontend/vite.config.ts` — Config con alias y proxy
- [x] `frontend/src/index.css` — Design system completo
- [x] `frontend/src/App.tsx` — Splash screen de estado
- [x] `frontend/Dockerfile` — Multi-stage (dev + build + nginx)
- [x] `docker/docker-compose.dev.yml` — Compose completo de desarrollo
- [x] `docker/.env.example` — Template de variables de entorno
- [x] `Ai/` — Todos los archivos de documentación del agente actualizados
- [ ] Crear virtualenv backend e instalar dependencias
- [ ] Crear virtualenv inference e instalar dependencias
- [ ] `npm install` frontend
- [ ] Verificación: `docker compose up postgres redis` arranca sin errores

---

## Fase 1 — Backend Core: Auth + API Base

**Objetivo:** Backend funcional con autenticación JWT, CRUD de usuarios, cámaras y zonas.

### Componentes a implementar

**Modelos ORM (SQLAlchemy):**
- `User` — roles: admin, supervisor, hse
- `Camera` — url rtsp, nombre, sede, estado
- `Zone` — polígono, cámara asociada, tipo de regla
- `Event` — tipo, severidad, cámara, timestamp, snapshot_path
- `Alert` — evento asociado, estado, revisado_por

**Endpoints:**
- `POST /api/v1/auth/login` — JWT access + refresh token
- `POST /api/v1/auth/refresh` — renovar access token
- `GET  /api/v1/auth/me` — datos del usuario autenticado
- `GET  /api/v1/cameras` — listar cámaras (paginado)
- `POST /api/v1/cameras` — crear cámara
- `GET  /api/v1/cameras/{id}` — detalle cámara
- `PUT  /api/v1/cameras/{id}` — actualizar cámara
- `DEL  /api/v1/cameras/{id}` — eliminar cámara
- `GET  /api/v1/zones` — zonas por cámara
- `POST /api/v1/zones` — crear zona (polígono)

**Migraciones Alembic:**
- Setup inicial de Alembic
- Migración 001: crear tablas base

---

## Fase 2 — Vision Pipeline: Ingesta + Detección + Tracking

**Objetivo:** Pipeline que lea video y detecte personas + EPP con YOLO + ByteTrack.

### Componentes
- `ingestion/worker.py` — lee RTSP/archivo, publica en Redis Streams
- `detection/yolo_detector.py` — wrapper Ultralytics YOLO
- `tracking/bytetrack_tracker.py` — wrapper ByteTrack via supervision
- `pipeline/video_processor.py` — orquesta ingestion → detection → tracking

---

## Fase 3 — Motor de Reglas SST

**Objetivo:** Convertir tracks en eventos estructurados de seguridad.

### Reglas a implementar
- `rules/ppe_rule.py` — EPP ausente sostenido N segundos
- `rules/zone_rule.py` — Invasión de zona de exclusión (polígono)
- `rules/fall_rule.py` — Caída (aspect ratio + inmovilidad)
- `rules/engine.py` — Motor que aplica todas las reglas por cámara

---

## Fase 4 — Alertas en Tiempo Real (WebSockets)

### Componentes
- `backend/app/api/v1/endpoints/ws.py` — WebSocket endpoint
- `backend/app/services/notification_service.py` — pub/sub Redis
- `backend/app/api/v1/endpoints/alerts.py` — CRUD de alertas

---

## Fase 5 — Frontend Dashboard

### Páginas
- Login
- Dashboard principal (cámaras + alertas activas)
- Historial de eventos
- Configuración de zonas (editor de polígonos)
- Gestión de cámaras
- Reportes

---

## Fase 6 — LLM: Reportes Narrativos

### Componentes
- `backend/app/services/llm_service.py` — generación de reportes
- `backend/app/api/v1/endpoints/reports.py` — endpoint de reportes
- `Ai/PROMPTS.md` — prompts del sistema

---

## Fase 7 — Hardening y Observabilidad

### Componentes
- Logging estructurado JSON en todos los servicios
- Health checks robustos (liveness + readiness)
- Métricas de latencia del pipeline
- Reconexión automática RTSP con backoff exponencial
- Docker Compose de producción con volúmenes persistentes

---

## v2.0 (Roadmap Futuro — según SAD)

- Analítica histórica y mapas de calor de riesgo
- Integración con control de acceso
- Soporte multi-sede (multi-tenant)
- Tracking multi-cámara con re-identificación

## v3.0 (Roadmap Futuro — según SAD)

- Modelos predictivos de riesgo
- Detección de fatiga y posturas ergonómicas
- Despliegue en dispositivos edge
