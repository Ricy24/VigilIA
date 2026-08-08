# ============================================================
# VigilIA — Inference Pipeline Dockerfile
# Multi-stage: base → development → production
#
# NOTA GPU: Para usar CUDA, cambiar la imagen base a:
#   pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime
# y asegurarse de tener el NVIDIA Container Toolkit instalado.
# ============================================================

# ---------- Base stage (CPU) ----------
FROM python:3.12-slim AS base

WORKDIR /app

# Dependencias del sistema para OpenCV y MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libgstreamer1.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

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

EXPOSE 8001

CMD ["python", "-m", "pipeline.main"]

# ---------- Production stage ----------
FROM base AS production

ENV ENVIRONMENT=production

COPY . .

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "-m", "pipeline.main"]
