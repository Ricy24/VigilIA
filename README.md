# VigilIA

**Visión artificial en tiempo real para Seguridad y Salud en el Trabajo.**

![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/Ultralytics-YOLO11-111F68)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

VigilIA convierte cámaras de videovigilancia convencionales en **sensores inteligentes de seguridad industrial**: detecta ausencia de EPP, invasión de zonas de exclusión, caídas y comportamientos anómalos, y emite alertas accionables con registro trazable.

No es un detector suelto. Es una plataforma completa: pipeline de visión, motor de reglas de negocio, API, alertas en vivo y trazabilidad de eventos.

---

## El problema

Una cámara de seguridad graba, pero no avisa. El cumplimiento de SST termina dependiendo de que alguien esté mirando el monitor en el momento exacto, y de un informe en Excel que se arma después.

VigilIA cierra ese hueco: el video se convierte en eventos con contexto (quién, dónde, qué regla se rompió, cuándo) y esos eventos llegan como alerta.

---

## Arquitectura

    Cámara IP / RTSP
          │
          ▼
    Inference (YOLO11 + ByteTrack)  ──►  Motor de reglas SST
          │                                     │
          ▼                                     ▼
       Eventos  ────────────────►  API FastAPI (v1)  ──►  PostgreSQL
                                        │
                                        ▼
                                  WebSocket  ──►  Dashboard React

---

## Estado del proyecto

| Fase | Alcance | Estado |
|------|---------|--------|
| 0 | Fundación: estructura, entornos, Docker | Completada |
| 1 | Backend core: auth, cámaras, zonas, eventos, alertas | En progreso |
| 2 | Pipeline de visión: YOLO + tracking | Prototipo funcional |
| 3 | Motor de reglas SST | Pendiente |
| 4 | Alertas en tiempo real (WebSocket) | Base lista |
| 5 | Dashboard React | Pendiente |
| 6 | Reportes asistidos por LLM | Pendiente |
| 7 | Hardening y despliegue | Pendiente |

### Qué funciona hoy

- **API REST v1** con endpoints de autenticación, cámaras, zonas, eventos, alertas y health check.
- **WebSocket** para empujar alertas al cliente.
- **Inferencia con YOLO11** (segmentación y pose estimation) corriendo sobre video real, con overlay de HUD.
- **Docker Compose** con PostgreSQL, Redis, backend e inference.

---

## Stack

- **Visión:** Python, OpenCV, Ultralytics YOLO11, ByteTrack, MediaPipe
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis, Alembic
- **Frontend:** React 18, Vite, TypeScript
- **Infraestructura:** Docker, Docker Compose

---

## Inicio rápido

    # 1. Variables de entorno
    cp docker/.env.example docker/.env

    # 2. Infraestructura + backend
    docker compose -f docker/docker-compose.dev.yml up postgres redis backend

    # 3. Frontend
    cd frontend && npm install && npm run dev

Dashboard: http://localhost:5173 · API docs: http://localhost:8000/docs

---

## Estructura

    VigilIA/
    ├── Ai/           Documentación técnica y de operación (leer primero)
    ├── backend/      FastAPI + PostgreSQL + Redis + Alembic
    ├── inference/    Pipeline de visión (YOLO11, tracking, reglas)
    ├── frontend/     React + Vite + TypeScript
    ├── docker/       Compose y variables de entorno
    ├── models/       Pesos YOLO (fuera de Git)
    ├── datasets/     Datasets de entrenamiento (fuera de Git)
    └── docs/         Documento de arquitectura (SAD v1.0)

---

## Documentación

| Documento | Contenido |
|-----------|-----------|
| [Ai/ARCHITECTURE.md](Ai/ARCHITECTURE.md) | Arquitectura del sistema |
| [Ai/ROADMAP.md](Ai/ROADMAP.md) | Hoja de ruta por fases |
| [Ai/TECH_STACK.md](Ai/TECH_STACK.md) | Stack con versiones |
| [Ai/DECISIONS.md](Ai/DECISIONS.md) | Registro de decisiones técnicas |
| [Ai/SECURITY.md](Ai/SECURITY.md) | Principios de seguridad |
| [docs/VigilIA_SAD_v1.0.docx](docs/VigilIA_SAD_v1.0.docx) | SAD completo |

---

## De CCTV a plataformas aéreas

El pipeline está diseñado para ser **independiente de la fuente de video**: consume un stream y devuelve detecciones con identidad persistente. Eso lo hace reutilizable en escenarios distintos al CCTV fijo.

Llevarlo a **video aéreo (drones)** requiere trabajo adicional y conocido:

- estabilización y compensación de movimiento de cámara,
- modelos entrenados con perspectiva aérea,
- georreferenciación de detecciones sobre el frame,
- cómputo en el borde (Jetson o similar).

Es una línea de trabajo del proyecto, no una capacidad ya integrada.

---

## Principio de seguridad

El sistema **detecta y alerta**. Nunca automatiza consecuencias sobre personas.

El LLM nunca decide si un evento es de seguridad: solo redacta narrativa de reportes. Ver [Ai/SECURITY.md](Ai/SECURITY.md).

---

## Autor

**Andrés Ricardo Durán Corredor** — Bogotá, Colombia
[GitHub](https://github.com/Ricy24) · [LinkedIn](https://www.linkedin.com/in/andres-duran-287462349/) · anriduco2019@gmail.com

Proyecto VigilIA, 2026.
