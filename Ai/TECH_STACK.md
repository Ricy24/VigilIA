# TECH_STACK.md — Stack Tecnológico de VigilIA

Versiones exactas utilizadas en el proyecto. Actualizar al cambiar dependencias.

---

## Backend

| Tecnología | Versión | Rol | Justificación (SAD §5) |
|------------|---------|-----|------------------------|
| Python | 3.12 | Lenguaje base | Ecosistema IA/ML; consistencia con inference |
| FastAPI | 0.115.6 | Web framework | Async, tipado fuerte, Swagger autogenerado |
| Pydantic | 2.10.3 | Validación de datos | Integración nativa FastAPI, modelos tipados |
| pydantic-settings | 2.6.1 | Configuración | Lectura de .env con validación de tipos |
| SQLAlchemy | 2.0.36 | ORM | Maduro, flexible, compatible con Alembic |
| Alembic | 1.14.0 | Migraciones DB | Estándar para SQLAlchemy |
| psycopg2-binary | 2.9.10 | Driver PostgreSQL | Estable, productivo |
| Redis (py) | 5.2.1 | Cliente Redis | Streams, cache, pub/sub |
| python-jose | 3.3.0 | JWT | Implementación JWT estándar |
| passlib[bcrypt] | 1.7.4 | Hashing contraseñas | bcrypt es el estándar de la industria |
| uvicorn[standard] | 0.32.1 | ASGI server | Servidor oficial recomendado para FastAPI |

## Inference Pipeline

| Tecnología | Versión | Rol | Justificación (SAD §5) |
|------------|---------|-----|------------------------|
| Python | 3.12 | Lenguaje base | Ecosistema IA/ML |
| OpenCV-python | 4.10.0.84 | Visión por computador | Estándar para procesamiento de video/imágenes |
| Ultralytics (YOLO) | 8.3.51 | Detección de objetos | YOLO11, mejor relación velocidad/precisión RT |
| PyTorch | 2.5.1 | Framework ML | Backend de Ultralytics |
| supervision | 0.25.0 | Tracking (ByteTrack) | Wrapper de ByteTrack, anotaciones, utilidades |
| MediaPipe | 0.10.18 | Estimación de pose | Detección de caídas (landmarks corporales) |
| NumPy | 1.26.4 | Operaciones matriciales | Base de todos los pipelines CV |

## Frontend

| Tecnología | Versión | Rol |
|------------|---------|-----|
| React | 18.3.1 | UI library |
| Vite | 6.0.5 | Build tool + dev server |
| TypeScript | 5.6.3 | Tipado estático |
| React Router | 6.28.0 | Enrutamiento SPA |
| TanStack Query | 5.62.7 | Server state management |
| Zustand | 5.0.2 | Client state management |
| Recharts | 2.13.3 | Gráficos y visualizaciones |
| Lucide React | 0.468.0 | Iconografía |
| date-fns | 4.1.0 | Manipulación de fechas |

## Infraestructura

| Tecnología | Versión | Rol |
|------------|---------|-----|
| Docker | ≥ 24.0 | Contenedores |
| Docker Compose | ≥ 2.24 | Orquestación local |
| PostgreSQL | 16-alpine | Base de datos relacional |
| Redis | 7-alpine | Cola de frames, cache, pub/sub |
| Nginx | alpine | Servidor estático (producción frontend) |

## Herramientas de Desarrollo

| Herramienta | Uso |
|-------------|-----|
| Git + GitHub | Control de versiones |
| Roboflow | Etiquetado de datasets (Fase 2+) |
| pytest | Tests Python (backend + inference) |
| ESLint | Linting TypeScript |

---

## Modelos de IA

| Modelo | Uso | Cuándo |
|--------|-----|--------|
| `yolo11n.pt` | Detección dev/pruebas (nano, rápido) | Fase 2 |
| `yolo11m.pt` | Detección producción (medium, balance) | Fase 2 |
| Fine-tuned YOLO | Detección EPP (casco, chaleco) | Fase 2+ |
| MediaPipe Pose | Estimación de pose para caídas | Fase 3 |
| GPT-4o-mini / Gemini | Generación de reportes narrativos | Fase 6 |

> **Nota:** Los modelos `.pt` y `.onnx` NO se almacenan en Git (`.gitignore`).
> Se descargan automáticamente por Ultralytics o se colocan manualmente en `models/`.
