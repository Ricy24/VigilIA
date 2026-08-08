"""
Modelos ORM de VigilIA — Fase 1

Importa todos los modelos para que Alembic los descubra
al generar migraciones automáticas.

Uso en alembic/env.py:
    from app.db.base import Base
    import app.db.models  # noqa: F401 — registra modelos en Base.metadata
"""

from app.db.models.user import User
from app.db.models.camera import Camera
from app.db.models.zone import Zone
from app.db.models.event import Event
from app.db.models.alert import Alert

__all__ = ["User", "Camera", "Zone", "Event", "Alert"]
