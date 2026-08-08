"""
VigilIA Backend — FastAPI Application Entry Point

Módulos registrados:
  - /api/v1/health  → Health check
  - /api/v1/auth    → Autenticación JWT (Fase 1)
  - /api/v1/cameras → CRUD de cámaras (Fase 1)
  - /ws             → WebSocket de alertas (Fase 4)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación."""
    # Startup
    print(f"🚀 VigilIA Backend iniciando — entorno: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    print("🛑 VigilIA Backend detenido")


app = FastAPI(
    title="VigilIA API",
    description=(
        "Plataforma inteligente de visión artificial para Seguridad y Salud "
        "en el Trabajo (SST). Detecta condiciones inseguras en tiempo real "
        "a partir de flujos de video de cámaras industriales."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
from app.api.v1.router import api_router  # noqa: E402

app.include_router(api_router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
@app.get("/", tags=["root"])
async def root():
    return {
        "service": "vigilia-backend",
        "version": "0.1.0",
        "docs": "/docs",
    }
