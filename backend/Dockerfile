# ============================================================
# VigilIA — Backend Dockerfile
# Multi-stage: base → development → production
# ============================================================

# ---------- Base stage ----------
FROM python:3.12-slim AS base

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Development stage ----------
FROM base AS development

ENV ENVIRONMENT=development

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------- Production stage ----------
FROM base AS production

ENV ENVIRONMENT=production \
    DEBUG=false

COPY . .

EXPOSE 8000

# Healthcheck integrado
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
