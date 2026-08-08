# DEPLOYMENT.md — Guía de Despliegue

---

## Desarrollo Local (sin Docker)

### Prerrequisitos
- Python 3.12
- Node.js 22+
- Docker Desktop (para PostgreSQL y Redis)
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/VigilIA.git
cd VigilIA
```

### 2. Levantar infraestructura (PostgreSQL + Redis)
```bash
docker compose -f docker/docker-compose.dev.yml up postgres redis -d
```

### 3. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Copiar variables de entorno
cp ../docker/.env.example .env  # Ajustar valores si es necesario

# Aplicar migraciones (Fase 1 en adelante)
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

Verificar: http://localhost:8000/docs

### 4. Inference Pipeline
```bash
cd inference
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cp ../docker/.env.example .env

python -m pipeline.main
```

### 5. Frontend
```bash
cd frontend
npm install
npm run dev
```

Verificar: http://localhost:5173

---

## Desarrollo con Docker Compose (recomendado)

```bash
# Copiar .env
cp docker/.env.example docker/.env

# Levantar todos los servicios base (postgres + redis + backend)
docker compose -f docker/docker-compose.dev.yml up postgres redis backend

# Con inference pipeline
docker compose -f docker/docker-compose.dev.yml --profile inference up

# Con frontend
docker compose -f docker/docker-compose.dev.yml --profile frontend up

# Todo junto
docker compose -f docker/docker-compose.dev.yml --profile inference --profile frontend up

# Ver logs de un servicio
docker compose -f docker/docker-compose.dev.yml logs -f backend

# Detener y eliminar volúmenes
docker compose -f docker/docker-compose.dev.yml down -v
```

---

## Producción (Fase 7)

> Pendiente de implementación en Fase 7 — Hardening.

Pasos previstos:
1. Configurar `docker/docker-compose.yml` de producción
2. Generar SECRET_KEY segura: `python -c "import secrets; print(secrets.token_hex(32))"`
3. Configurar ALLOWED_ORIGINS con el dominio real
4. Usar Nginx como reverse proxy
5. Configurar volúmenes persistentes para PostgreSQL y Redis
6. Habilitar backups automáticos de PostgreSQL

---

## Variables de Entorno Críticas para Producción

| Variable | Valor por defecto (dev) | ⚠️ Producción |
|----------|------------------------|--------------|
| `SECRET_KEY` | String largo placeholder | Cambiar: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `POSTGRES_PASSWORD` | `vigilia_dev_pass` | Usar contraseña segura (20+ chars) |
| `ENVIRONMENT` | `development` | `production` |
| `DEBUG` | `true` | `false` |
| `ALLOWED_ORIGINS` | localhost | Dominio real del frontend |
| `DEVICE` | `cpu` | `cuda` si hay GPU |

---

## Migraciones de Base de Datos (Fase 1 en adelante)

```bash
# Crear nueva migración
cd backend
alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history

# Revertir una migración
alembic downgrade -1
```
