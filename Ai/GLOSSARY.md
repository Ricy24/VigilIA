# GLOSSARY.md — Glosario de VigilIA

Términos técnicos y de SST utilizados en el proyecto.

---

## Términos de SST (Seguridad y Salud en el Trabajo)

| Término | Definición |
|---------|-----------|
| **SST** | Seguridad y Salud en el Trabajo — disciplina y marco normativo para prevenir accidentes laborales |
| **HSE** | Health, Safety and Environment — equivalente anglosajón de SST, rol del profesional de seguridad |
| **EPP** | Elementos de Protección Personal — casco, chaleco reflectivo, guantes, gafas de seguridad, etc. |
| **LOTO** | Lockout/Tagout — procedimiento de bloqueo y etiquetado de maquinaria para mantenimiento seguro |
| **Zona de exclusión** | Área delimitada donde el acceso está restringido o requiere condiciones específicas de seguridad |
| **ARL** | Administradora de Riesgos Laborales (Colombia) — entidad que gestiona el seguro de accidentes |
| **Acto inseguro** | Comportamiento de una persona que aumenta el riesgo de accidente |
| **Condición insegura** | Estado del entorno físico que genera riesgo de accidente |
| **Incidente** | Evento que pudo haber causado accidente pero no lo causó (near miss) |
| **SG-SST** | Sistema de Gestión de SST — marco documental y operativo exigido por ley en Colombia |
| **Decreto 1072** | Decreto Único Reglamentario del Sector Trabajo (Colombia 2015) — marco legal del SG-SST |
| **Resolución 0312** | Estándares mínimos del SG-SST según tamaño de empresa (Colombia 2019) |

---

## Términos de Visión Artificial

| Término | Definición |
|---------|-----------|
| **RTSP** | Real Time Streaming Protocol — protocolo para transmitir video desde cámaras IP |
| **NVR** | Network Video Recorder — grabador de video en red, almacena el flujo de cámaras IP |
| **YOLO** | You Only Look Once — familia de modelos de detección de objetos en una sola pasada de red |
| **Bounding box** | Rectángulo que delimita un objeto detectado en la imagen |
| **Confidence score** | Valor 0-1 que indica la certeza del modelo sobre una detección |
| **IoU** | Intersection over Union — métrica de superposición entre dos rectángulos |
| **NMS** | Non-Maximum Suppression — algoritmo para eliminar detecciones duplicadas del mismo objeto |
| **mAP** | Mean Average Precision — métrica estándar de evaluación de detectores de objetos |
| **Fine-tuning** | Técnica de Transfer Learning: adaptar un modelo preentrenado a nuevas clases con pocos datos |
| **Tracking** | Seguimiento de objetos a lo largo del tiempo, asignando IDs persistentes entre frames |
| **ByteTrack** | Algoritmo de tracking multiobjeto que incluye detecciones de baja confianza en la asociación |
| **DeepSORT** | Algoritmo de tracking que usa embeddings de apariencia para re-identificación |
| **Track** | Objeto en seguimiento con ID persistente, bounding box y trayectoria histórica |
| **Trayectoria** | Secuencia histórica de posiciones de un track a lo largo del tiempo |
| **MediaPipe** | Framework de Google para estimación de pose corporal (landmarks) |
| **FPS** | Frames Per Second — cuadros por segundo de video procesados por el pipeline |
| **BGR / RGB** | Orden de canales de color: OpenCV usa BGR, la mayoría de librerías ML esperan RGB |
| **COCO** | Common Objects in Context — dataset de referencia con 80 clases, usado para preentrenamiento de YOLO |
| **Roboflow** | Plataforma para gestión, etiquetado y versioning de datasets de visión artificial |

---

## Términos de Arquitectura

| Término | Definición |
|---------|-----------|
| **Redis Streams** | Estructura de datos de Redis para colas de mensajes persistentes con consumer groups |
| **WebSocket** | Protocolo de comunicación full-duplex entre servidor y cliente para eventos en tiempo real |
| **Pub/Sub** | Patrón publicador/suscriptor para distribuir eventos a múltiples consumidores |
| **Alembic** | Herramienta de migraciones de base de datos para SQLAlchemy |
| **Pydantic** | Librería Python para validación de datos y serialización con type hints |
| **ASGI** | Asynchronous Server Gateway Interface — estándar de servidores async para Python (usado por FastAPI) |
| **JWT** | JSON Web Token — estándar para autenticación stateless mediante tokens firmados |
| **Hot-reload** | Recarga automática del servidor al detectar cambios en el código fuente (desarrollo) |
| **Multi-stage build** | Técnica Dockerfile que usa etapas separadas para construir y servir, reduciendo tamaño de imagen |

---

## Abreviaciones usadas en el código

| Abreviación | Significado |
|-------------|------------|
| `ppe` | Personal Protective Equipment (EPP en inglés, usado en nombres de código) |
| `bbox` | Bounding box |
| `conf` | Confidence score |
| `fps` | Frames per second |
| `rt` | Real-time |
| `ws` | WebSocket |
| `db` | Database |
| `stt` / `sst` | Seguridad y Salud en el Trabajo |
