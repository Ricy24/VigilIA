# ARCHITECTURE.md — Arquitectura de VigilIA

Basado en: SAD v1.0 §4 — Arquitectura General

---

## Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CÁMARAS IP (RTSP)                            │
│    Cam-01    Cam-02    Cam-03    ...    Cam-N                        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ RTSP stream
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 INFERENCE PIPELINE  (Docker)                         │
│                                                                     │
│  ┌───────────────┐                                                  │
│  │  Ingestion    │──► Redis Streams (frames)                        │
│  │  Worker       │    (1 worker por cámara)                         │
│  └───────────────┘                                                  │
│         ▼                                                           │
│  ┌───────────────┐   ┌──────────────┐   ┌────────────────────────┐ │
│  │  YOLO         │──►│  ByteTrack   │──►│  Motor de Reglas SST   │ │
│  │  Detector     │   │  Tracker     │   │  - EPP ausente         │ │
│  │  (personas +  │   │  (IDs pers.) │   │  - Zona exclusión      │ │
│  │   EPP)        │   │              │   │  - Caída               │ │
│  └───────────────┘   └──────────────┘   └──────────┬─────────────┘ │
└─────────────────────────────────────────────────────┼───────────────┘
                                                      │ HTTP (evento)
                                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND  FastAPI  (Docker)                        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────────┐  ┌────────────────────┐   │
│  │  API REST    │  │  Alert Service   │  │  Notification      │   │
│  │  /auth       │  │  (persistencia   │  │  Service           │   │
│  │  /cameras    │  │   de eventos)    │  │  (WebSocket +      │   │
│  │  /zones      │  │                  │  │   Redis pub/sub)   │   │
│  │  /alerts     │  │                  │  │                    │   │
│  │  /reports    │  └──────────────────┘  └─────────┬──────────┘   │
│  └──────┬───────┘                                   │             │
│         │                   ┌───────────────────────┘             │
│         ▼                   ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                PostgreSQL  (Docker)                         │   │
│  │   users │ cameras │ zones │ events │ alerts │ reports       │   │
│  └────────────────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                Redis  (Docker)                              │   │
│  │   Streams (frames) │ Cache │ Pub/Sub (alertas WS)          │   │
│  └────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ REST API + WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 FRONTEND  React + Vite  (Docker / CDN)              │
│                                                                     │
│   Login → Dashboard → Alertas RT → Historial → Zonas → Reportes    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP (eventos estructurados)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              LLM SERVICE  (Fase 6 — externo o embebido)             │
│   Recibe eventos estructurados → genera narrativa de turno          │
│   NUNCA decide si algo es o no un evento de seguridad               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Capas de la Arquitectura

Según SAD §4.3 — Principio de separación estricta entre capas:

| Capa | Módulo | Responsabilidad | NO conoce |
|------|--------|-----------------|-----------|
| Captura | ingestion/worker.py | Leer RTSP, publicar frames | Detección, reglas, usuarios |
| Percepción | detection/, tracking/ | Frames → detecciones → tracks | Usuarios, BD, alertas |
| Dominio | rules/engine.py | Tracks → eventos SST | Cómo se detectó, cómo notifica |
| Aplicación | backend/app/ | Persistencia, auth, notificaciones | Pipeline de CV |
| Presentación | frontend/ | UI, interacción usuario | Lógica de negocio |

---

## Contratos de Interfaz entre Módulos

### Ingestion → Vision Pipeline
- **Canal:** Redis Streams (`vigilia:frames:{camera_id}`)
- **Payload:** `{ frame_id, camera_id, timestamp, frame_bytes (base64 o referencia) }`
- **Política:** Descarta frames antiguos si el pipeline se atrasa (prioriza RT)

### Vision Pipeline → Backend
- **Canal:** HTTP POST `/api/v1/internal/events`
- **Payload:** Evento estructurado (ver esquema en Fase 3)

### Backend → Frontend
- **Canal 1:** REST API (CRUD, historial paginado)
- **Canal 2:** WebSocket (`ws://backend/ws`) para push de alertas en tiempo real

### Backend → LLM Service
- **Canal:** HTTP POST con batch de eventos del período
- **Restricción:** El prompt siempre incluye los datos reales, nunca pregunta al LLM si algo es riesgo

---

## Principios de Diseño (SAD §4.7)

1. **Single Responsibility por servicio** — cada microservicio tiene una única razón de cambio
2. **Stateless donde sea posible** — el backend no mantiene sesión en memoria local
3. **Fail-safe, no fail-silent** — caída de cámara genera evento operativo, no silencio
4. **Backpressure explícito** — colas absorben picos, descartan frames redundantes conscientemente
5. **Desacoplamiento por contrato** — JSON schemas versionados, no código compartido entre servicios
