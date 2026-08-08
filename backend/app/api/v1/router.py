"""Router principal v1 — agrega todos los sub-routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

# Health check — siempre disponible, sin autenticación
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Los siguientes routers se agregan en las fases correspondientes:
# Fase 1: auth, cameras, zones, users
# Fase 4: websocket de alertas
