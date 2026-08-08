# PROJECT_CONTEXT.md — Contexto del Proyecto VigilIA

## Resumen

VigilIA es una plataforma inteligente de visión por computador e inteligencia artificial diseñada
para transformar las cámaras de seguridad tradicionales en un sistema capaz de interpretar lo que
ocurre en tiempo real y apoyar la prevención de riesgos laborales.

Su propósito es analizar continuamente el entorno utilizando modelos de inteligencia artificial para
detectar personas, equipos de protección personal (EPP), zonas de riesgo, caídas, posturas inseguras
y otros eventos relevantes para la Seguridad y Salud en el Trabajo (SST). A partir de esta información,
VigilIA genera alertas, registra eventos y produce reportes que ayudan a supervisores y empresas a
tomar decisiones rápidas y fundamentadas.

---

## Documento de referencia

- **SAD:** `docs/VigilIA_SAD_v1.0.docx` — Software Architecture Document v1.0 (Andrés Durán, Julio 2026)
- **675 líneas, 135KB** — cubre introducción, análisis, arquitectura, tecnologías, visión artificial,
  datasets, entrenamiento, motor de reglas, roadmap y diario de ingeniería.

---

## Problema que resuelve

Las organizaciones ya invirtieron en infraestructura de videovigilancia (cámaras IP, NVR) pero el video
nunca se analiza en tiempo real. Se almacena y solo se revisa cuando ya ocurrió un accidente.

Limitaciones del CCTV tradicional:
- **Cobertura humana limitada:** un supervisor no puede monitorear 40 cámaras 8 horas seguidas
- **Video como archivo, no señal:** se trata como evidencia forense post-hoc, no como datos analizables
- **Supervisión manual costosa:** rondas frecuentes requieren personal exclusivo, dejan ventanas sin cobertura
- **Efecto Hawthorne:** comportamiento de riesgo cuando el supervisor no está presente

---

## Solución

VigilIA procesa flujos de video en tiempo real con IA para detectar:
- Ausencia de EPP (casco, chaleco reflectivo, guantes, gafas)
- Invasión de zonas de exclusión (maquinaria en movimiento, áreas restringidas)
- Caídas y personas inmóviles en el suelo
- Aglomeraciones peligrosas y cruces de trayectoria

Genera alertas inmediatas dirigidas al supervisor correcto y mantiene un registro estructurado y
auditable de cada evento.

---

## Estado del Proyecto

**Fase actual:** Fase 0 — Fundación completada ✅

| Fase | Estado |
|------|--------|
| 0 — Fundación | ✅ Completada |
| 1 — Backend Core | ⏳ Próxima |
| 2 — Vision Pipeline | ⏳ Pendiente |
| 3 — Motor de Reglas | ⏳ Pendiente |
| 4 — WebSockets | ⏳ Pendiente |
| 5 — Frontend Dashboard | ⏳ Pendiente |
| 6 — LLM Reports | ⏳ Pendiente |
| 7 — Hardening | ⏳ Pendiente |

---

## Stack Tecnológico

Ver `Ai/TECH_STACK.md` para versiones exactas.

- **Vision Pipeline:** Python 3.12 + OpenCV + Ultralytics YOLO11 + ByteTrack + MediaPipe
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL + Redis
- **Frontend:** React 18 + Vite + TypeScript
- **Infraestructura:** Docker + Docker Compose

---

## Equipo

- **Autor del SAD y desarrollador principal:** Andrés Durán
- **Contexto:** Proyecto para concurso de IA — SENA / investigación académica

---

## Repositorio

GitHub: `Ricy24/VigilIA`
