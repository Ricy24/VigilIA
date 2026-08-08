# VigilIA

**Plataforma Inteligente de Visión Artificial para Seguridad y Salud en el Trabajo (SST)**

[![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)](.)
[![Fase](https://img.shields.io/badge/fase-0%20fundaci%C3%B3n-blue)](Ai/ROADMAP.md)
[![Python](https://img.shields.io/badge/python-3.12-blue)](backend/requirements.txt)
[![React](https://img.shields.io/badge/react-18-61dafb)](frontend/package.json)

VigilIA convierte cámaras de videovigilancia convencionales en sensores inteligentes de SST,
detectando en tiempo real: ausencia de EPP, invasión de zonas de exclusión, caídas y comportamientos
anómalos. Genera alertas accionables y registros trazables para la gestión de seguridad industrial.

---

## 🏗️ Estado del Proyecto

| Fase | Nombre | Estado |
|------|--------|--------|
| 0 | Fundación (estructura, entornos, Docker) | ✅ Completada |
| 1 | Backend Core (Auth, CRUD, DB) | ⏳ Próxima |
| 2 | Vision Pipeline (YOLO + ByteTrack) | ⏳ Pendiente |
| 3 | Motor de Reglas SST | ⏳ Pendiente |
| 4 | Alertas WebSocket | ⏳ Pendiente |
| 5 | Frontend Dashboard | ⏳ Pendiente |
| 6 | LLM Reports | ⏳ Pendiente |
| 7 | Hardening | ⏳ Pendiente |

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker Desktop
- Python 3.12
- Node.js 22+

### Levantar infraestructura de desarrollo

```bash
# 1. Copiar variables de entorno
cp docker/.env.example docker/.env

# 2. Levantar PostgreSQL + Redis + Backend
docker compose -f docker/docker-compose.dev.yml up postgres redis backend

# 3. Frontend (en otra terminal)
cd frontend && npm install && npm run dev
```

Abrir: http://localhost:5173 | API Docs: http://localhost:8000/docs

---

## 📁 Estructura del Proyecto

```
VigilIA/
├── Ai/           ← Documentación del agente de IA (leer primero)
├── backend/      ← FastAPI + PostgreSQL + Redis
├── inference/    ← Vision Pipeline (YOLO + ByteTrack + Reglas SST)
├── frontend/     ← React + Vite + TypeScript
├── docker/       ← Docker Compose + variables de entorno
├── models/       ← Modelos YOLO (.pt) — ignorados por Git
├── datasets/     ← Datasets de entrenamiento — ignorados por Git
└── docs/         ← Documentación (SAD v1.0)
```

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [Ai/AI_AGENT.md](Ai/AI_AGENT.md) | Guía de operación para agentes de IA |
| [Ai/ROADMAP.md](Ai/ROADMAP.md) | Hoja de ruta detallada |
| [Ai/ARCHITECTURE.md](Ai/ARCHITECTURE.md) | Arquitectura del sistema |
| [Ai/TECH_STACK.md](Ai/TECH_STACK.md) | Stack tecnológico con versiones |
| [Ai/DECISIONS.md](Ai/DECISIONS.md) | Registro de decisiones técnicas |
| [Ai/DEPLOYMENT.md](Ai/DEPLOYMENT.md) | Guía de despliegue |
| [docs/VigilIA_SAD_v1.0.docx](docs/VigilIA_SAD_v1.0.docx) | SAD completo (referencia arquitectónica) |

---

## 🛠️ Stack Tecnológico

- **Vision Pipeline:** Python + OpenCV + Ultralytics YOLO11 + ByteTrack + MediaPipe
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL + Redis
- **Frontend:** React 18 + Vite + TypeScript
- **Infraestructura:** Docker + Docker Compose

---

## ⚠️ Principio de Seguridad Fundamental

El sistema de IA **detecta y alerta**. **Nunca automatiza consecuencias** sobre personas.
El LLM **nunca decide** si algo es un evento de seguridad — solo genera narrativa de reportes.
Ver [Ai/SECURITY.md](Ai/SECURITY.md) y [Ai/DECISIONS.md](Ai/DECISIONS.md).

---

## 👤 Autor

Andrés Durán — Proyecto VigilIA, 2026
