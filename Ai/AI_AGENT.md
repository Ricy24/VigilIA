# AI_AGENT.md — Instrucciones para el Agente de IA

> Este archivo es la guía de operación para cualquier agente de IA que trabaje en el repositorio VigilIA.
> Léelo siempre al inicio de cualquier sesión antes de modificar código.

---

## 1. Contexto del Proyecto

**VigilIA** es una plataforma de visión artificial para Seguridad y Salud en el Trabajo (SST).
Detecta en tiempo real: ausencia de EPP, invasión de zonas de exclusión, caídas y comportamientos anómalos
en cámaras de videovigilancia industriales.

- **SAD de referencia:** `docs/VigilIA_SAD_v1.0.docx` — fuente de verdad arquitectónica.
- **Fase actual:** Ver `Ai/ROADMAP.md` → sección "Estado Actual".
- **Tareas pendientes:** Ver `Ai/TASKS.md`.
- **Decisiones tomadas:** Ver `Ai/DECISIONS.md` antes de proponer cambios de arquitectura.

---

## 2. Reglas Críticas de Seguridad del Sistema

> [!CAUTION]
> Estas reglas no son opcionales. El sistema toma decisiones sobre seguridad de personas.

1. **El LLM NUNCA decide eventos de seguridad.** Solo narra y resume eventos ya detectados y
   estructurados por el Vision Pipeline. Si algún código propone usar el LLM para evaluar si
   algo es o no un riesgo, es un error de diseño grave.

2. **Minimizar falsos negativos en riesgo alto.** Ante la disyuntiva de umbral, calibrar hacia
   más alertas (falsos positivos revisables por humano) antes que perder condiciones reales
   de riesgo.

3. **Human-in-the-loop.** Ninguna consecuencia sobre una persona (sanción, reporte formal)
   se automatiza completamente. El sistema detecta y alerta; la decisión final es humana.

4. **Privacidad por diseño.** No se almacena más información personal de la necesaria para SST.
   En Colombia aplica Ley 1581 de 2012 (habeas data).

---

## 3. Estructura del Repositorio

```
VigilIA/
├── Ai/                     ← Documentación del agente (AQUÍ estás)
├── backend/                ← FastAPI + PostgreSQL + Redis
│   ├── app/
│   │   ├── api/v1/         ← Endpoints REST
│   │   ├── core/           ← Config, seguridad, JWT
│   │   ├── db/             ← SQLAlchemy, sesión, modelos ORM
│   │   ├── schemas/        ← Pydantic schemas (request/response)
│   │   └── services/       ← Lógica de negocio
│   ├── Dockerfile
│   └── requirements.txt
├── inference/              ← Vision Pipeline (YOLO + ByteTrack + Reglas)
│   ├── pipeline/
│   │   ├── ingestion/      ← Workers RTSP → Redis Streams
│   │   ├── detection/      ← Wrapper YOLO
│   │   ├── tracking/       ← Wrapper ByteTrack
│   │   └── rules/          ← Motor de reglas SST
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               ← React + Vite + TypeScript
│   ├── src/
│   │   ├── components/     ← Componentes reutilizables
│   │   ├── pages/          ← Páginas del dashboard
│   │   ├── hooks/          ← Custom hooks (WebSocket, queries)
│   │   ├── services/       ← API client (httpx)
│   │   ├── stores/         ← Estado global (Zustand)
│   │   └── types/          ← TypeScript interfaces
│   └── Dockerfile
├── docker/
│   ├── docker-compose.dev.yml
│   └── .env.example
├── models/                 ← Modelos YOLO (.pt, .onnx) — en .gitignore
├── datasets/               ← Datasets de entrenamiento — en .gitignore
├── docs/                   ← Documentación (SAD, diagramas)
└── tests/                  ← Tests de integración E2E
```

---

## 4. Flujo de Trabajo del Agente

### Al iniciar una sesión:
1. Leer `Ai/TASKS.md` para ver qué hay en progreso
2. Leer `Ai/ROADMAP.md` para conocer la fase actual
3. Leer `Ai/DECISIONS.md` para no re-debatir decisiones ya tomadas
4. Si hay cambios de arquitectura, revisar el SAD antes de proponer

### Al finalizar una sesión:
1. Actualizar `Ai/TASKS.md` con el estado real de las tareas
2. Registrar cualquier decisión técnica nueva en `Ai/DECISIONS.md`
3. Actualizar `Ai/ROADMAP.md` si una fase avanzó
4. Si se cambiaron dependencias, actualizar `Ai/TECH_STACK.md`

---

## 5. Comandos Frecuentes

```bash
# Levantar infraestructura de desarrollo (postgres + redis + backend)
docker compose -f docker/docker-compose.dev.yml up postgres redis backend

# Solo infraestructura de datos
docker compose -f docker/docker-compose.dev.yml up postgres redis

# Frontend local (sin Docker)
cd frontend && npm run dev

# Backend local (sin Docker)
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Inference local (sin Docker)
cd inference
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pipeline.main

# Migraciones (Fase 1 en adelante)
cd backend
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

---

## 6. Convenciones de Código

Ver `Ai/CODING_STANDARDS.md` para el detalle completo.

Resumen:
- Python: PEP 8, type hints obligatorios, docstrings en módulos y clases públicas
- TypeScript: strict mode, interfaces preferidas sobre types para objetos
- Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- No se mergea código sin tests en los módulos críticos (detection, rules, auth)
