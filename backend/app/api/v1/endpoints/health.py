"""
Health check endpoint.

Verifica el estado de la aplicación y sus dependencias críticas.
Usado por Docker health checks y sistemas de monitoreo.

GET /api/v1/health      → estado rápido (sin verificar deps)
GET /api/v1/health/full → estado completo (verifica DB y Redis)
"""

import time
from typing import Dict, Any

import redis as redis_lib
from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

router = APIRouter()

START_TIME = time.time()


@router.get("", summary="Health check básico")
async def health_check() -> Dict[str, Any]:
    """
    Responde 200 inmediatamente si el servicio está corriendo.
    No verifica dependencias externas — útil para load balancers.
    """
    return {
        "status": "ok",
        "service": "vigilia-backend",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }


@router.get("/full", summary="Health check completo")
async def health_check_full() -> Dict[str, Any]:
    """
    Verifica la conectividad con PostgreSQL y Redis.
    Responde 200 si todo está bien, 503 si alguna dependencia falla.
    """
    checks: Dict[str, Any] = {}

    # --- PostgreSQL ---
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["postgres"] = {"status": "ok"}
    except Exception as e:
        checks["postgres"] = {"status": "error", "detail": str(e)}

    # --- Redis ---
    try:
        r = redis_lib.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        r.ping()
        checks["redis"] = {"status": "ok"}
    except Exception as e:
        checks["redis"] = {"status": "error", "detail": str(e)}

    all_ok = all(v["status"] == "ok" for v in checks.values())

    return {
        "status": "ok" if all_ok else "degraded",
        "service": "vigilia-backend",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "checks": checks,
    }
