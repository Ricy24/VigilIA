# DECISIONS.md — Registro de Decisiones Técnicas

> Este archivo registra las decisiones técnicas importantes tomadas durante el desarrollo de VigilIA,
> con su contexto, alternativas consideradas y justificación. Sirve para evitar re-debatir decisiones
> ya tomadas y entender el "por qué" detrás de cada elección.

Formato: `[FECHA] [ÁREA] Título de la decisión`

---

## [2026-08-08] [ARQUITECTURA] Microservicios ligeros sobre monolito

**Decisión:** VigilIA se construye como microservicios (backend, inference, frontend, cada uno en su
propio contenedor Docker) en lugar de un monolito.

**Contexto:** El pipeline de visión artificial tiene requerimientos muy distintos al backend REST:
necesita drivers de GPU, librerías de CV pesadas, y escala en dimensión de cámaras independientemente
de la carga HTTP del backend.

**Alternativas consideradas:**
- Monolito Python con todos los componentes (más simple de desarrollar, pero acoplamiento excesivo
  entre CV y API, dificulta el escalado y los despliegues on-premise)

**Justificación:** La separación permite escalar los workers de inferencia independientemente del
backend, cambiar el modelo de detección sin afectar la API, y desplegar en hardware diferente
(GPU para inference, CPU normal para backend). Referencia: SAD §4.

---

## [2026-08-08] [CV] YOLO (Ultralytics) como detector principal

**Decisión:** Usar la librería Ultralytics con modelos YOLO11 como detector de objetos en el
Vision Pipeline.

**Alternativas consideradas:**
- Faster R-CNN (mayor precisión, demasiado lento para RT con múltiples cámaras)
- DETR y variantes Transformer (buena precisión, mayor costo computacional, menos maduro para prod)
- Detectron2 (excelente, pero ecosistema más complejo y curva de aprendizaje alta)

**Justificación:** YOLO ofrece el mejor balance velocidad/precisión para detección en tiempo real.
Ultralytics es la implementación más madura y documentada, con herramientas de fine-tuning accesibles.
La clase "persona" ya tiene alta precisión preentrenada en COCO. Referencia: SAD §5.3 y §7.3.

---

## [2026-08-08] [CV] ByteTrack (via supervision) como tracker principal

**Decisión:** Usar ByteTrack, disponible a través de la librería `supervision` de Roboflow,
como algoritmo de tracking multiobjeto por defecto.

**Alternativas consideradas:**
- DeepSORT (mayor robustez en oclusiones largas, pero mayor costo computacional por inferencia adicional
  de red de re-identificación). Se mantiene como alternativa configurable para zonas de alta densidad.

**Justificación:** ByteTrack incluye detecciones de baja confianza en la asociación, reduciendo
fragmentación de tracks en condiciones industriales con oclusiones parciales. Menor costo que DeepSORT.
Referencia: SAD §5.4 y §8.4.

---

## [2026-08-08] [BACKEND] FastAPI sobre Django

**Decisión:** Usar FastAPI + SQLAlchemy + Alembic en lugar de Django REST Framework.

**Justificación:** FastAPI es async-first (crucial para WebSockets concurrentes), tiene tipado fuerte
con Pydantic v2, y es el mismo lenguaje que el inference pipeline facilitando compartir tipos.
Django es más opinado y monolítico, menos natural para arquitectura de microservicios.
Referencia: SAD §5.7.

---

## [2026-08-08] [DB] PostgreSQL sobre MongoDB

**Decisión:** PostgreSQL 16 como base de datos principal.

**Justificación:** Los eventos de seguridad tienen implicaciones legales → se necesitan garantías ACID.
El soporte JSONB de PostgreSQL permite metadatos semi-estructurados sin sacrificar transaccionalidad.
MongoDB sacrifica consistencia transaccional que es crítica para el historial de incidentes.
Referencia: SAD §5.8.

---

## [2026-08-08] [INFRA] Redis para cola de frames (Streams) y pub/sub

**Decisión:** Redis cumple tres roles: cola de frames (Redis Streams), cache y pub/sub para WebSockets.

**Alternativas consideradas:**
- RabbitMQ: más robusto para mensajería, pero mayor complejidad operativa injustificada en la v1.0
- Kafka: excelente para escala muy alta, overkill para la escala inicial

**Justificación:** Redis resuelve los tres casos de uso con un solo componente de infraestructura,
manteniendo la simplicidad operativa de la v1.0. Kafka queda como migración futura para escala alta.
Referencia: SAD §5.11.

---

## [2026-08-08] [FRONTEND] React + Vite + TypeScript sobre Vue/Angular

**Decisión:** React 18 con Vite como bundler y TypeScript strict.

**Justificación:** Ecosistema más maduro, mayor disponibilidad de librerías (Recharts, TanStack Query),
y el dashboard de VigilIA se beneficia del modelo de componentes de React para widgets independientes.
Vite ofrece HMR extremadamente rápido para desarrollo.
Referencia: SAD §5.9.

---

## [2026-08-08] [SEGURIDAD] LLM nunca en decisiones de seguridad

**Decisión:** El módulo LLM es estrictamente post-hoc: solo recibe eventos YA detectados y
estructurados por el Vision Pipeline para generar narrativa. Nunca participa en decidir si
algo es o no un evento de seguridad.

**Justificación:** Los LLM pueden alucinar. Una alucinación en una decisión de seguridad (generar
un evento falso o ignorar uno real) puede tener consecuencias sobre la vida de personas.
La separación estricta entre detección (pipeline determinista) y narración (LLM) es un principio
de diseño no negociable. Referencia: SAD §5.14, §14 (principio de separación estricta).

---

## [2026-08-08] [PROCESO] Desarrollo incremental por fases

**Decisión:** El desarrollo se hace en fases pequeñas (0→7), cada una con entregables verificables,
en lugar de intentar construir todo de una vez.

**Justificación:** Sistema complejo con múltiples capas interdependientes. Las fases permiten validar
cada capa antes de construir sobre ella, reducen el riesgo de deuda técnica acumulada, y permiten
tener siempre un sistema parcialmente funcional en lugar de nada durante meses.
