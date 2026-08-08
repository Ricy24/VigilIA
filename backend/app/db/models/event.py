"""
Modelo ORM: Event

Representa un evento de SST detectado por el Vision Pipeline.
Es el registro inmutable de "algo detectado" — no tiene estado porque
no cambia una vez creado. El estado lo gestiona la Alerta asociada.

Tipos de evento:
  - ppe_violation    → persona sin EPP requerido
  - zone_intrusion   → persona en zona de exclusión
  - fall_detected    → posible caída (persona en suelo > N segundos)
  - camera_offline   → cámara perdió conexión (evento operativo)
  - person_detected  → detección genérica (para monitoreo, sin regla específica)

Severidades (alineadas con jerarquía de controles de SST):
  - low      → informativo
  - medium   → requiere atención dentro del turno
  - high     → requiere atención inmediata
  - critical → riesgo de vida, prioridad máxima
"""

import enum
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EventType(str, enum.Enum):
    PPE_VIOLATION = "ppe_violation"
    ZONE_INTRUSION = "zone_intrusion"
    FALL_DETECTED = "fall_detected"
    CAMERA_OFFLINE = "camera_offline"
    PERSON_DETECTED = "person_detected"


class EventSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    camera_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True, index=True
    )
    zone_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("zones.id", ondelete="SET NULL"), nullable=True, index=True
    )

    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="eventtype"), nullable=False, index=True
    )
    severity: Mapped[EventSeverity] = mapped_column(
        Enum(EventSeverity, name="eventseverity"), nullable=False, index=True
    )

    # ID persistente del track en la sesión del pipeline (ByteTrack ID)
    track_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Confianza de la detección (0.0 - 1.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Duración del evento en segundos (para alertas de duración sostenida)
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Snapshot y evidencia
    snapshot_path: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Bounding box del objeto principal: {"x1": 0.1, "y1": 0.1, "x2": 0.5, "y2": 0.8}
    bounding_box: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Metadatos adicionales semi-estructurados (EPP faltante, etc.)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata", JSON, nullable=True
    )

    # Descripción generada automáticamente por el motor de reglas
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamp exacto del evento (puede diferir de created_at por latencia del pipeline)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relaciones
    camera: Mapped["Camera"] = relationship("Camera", back_populates="events")  # noqa: F821
    alert: Mapped["Alert | None"] = relationship("Alert", back_populates="event", uselist=False)  # noqa: F821

    def __repr__(self) -> str:
        return (
            f"<Event id={self.id} type={self.event_type} "
            f"severity={self.severity} cam={self.camera_id}>"
        )
