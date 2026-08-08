"""
Modelo ORM: Alert

Representa el estado mutable de un evento detectado.
Mientras Event es inmutable (registro de "qué pasó"),
Alert es el ciclo de vida de la respuesta al evento.

Estados:
  - pending   → generada, sin revisar
  - reviewing → supervisor la vio, está investigando
  - resolved  → revisada y cerrada (acción tomada)
  - dismissed → falso positivo, descartada por el supervisor
"""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AlertStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        unique=True,  # Relación 1:1 con Event
        nullable=False,
        index=True,
    )

    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, name="alertstatus"),
        nullable=False,
        default=AlertStatus.PENDING,
        index=True,
    )

    # Usuario que revisó/resolvió la alerta (FK a users.id)
    reviewed_by_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Notas del supervisor al resolver/descartar
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relaciones
    event: Mapped["Event"] = relationship("Event", back_populates="alert")  # noqa: F821
    reviewed_by: Mapped["User | None"] = relationship("User")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Alert id={self.id} event_id={self.event_id} status={self.status}>"
