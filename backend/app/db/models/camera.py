"""
Modelo ORM: Camera

Representa una cámara IP registrada en el sistema.
Cada cámara tiene una URL RTSP y pertenece a una sede.

Estados posibles:
  - active    → pipeline procesando activamente
  - inactive  → registrada pero no procesando
  - error     → pipeline detectó falla de conexión
"""

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CameraStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    site: Mapped[str] = mapped_column(String(255), nullable=False)  # Sede / planta

    rtsp_url: Mapped[str] = mapped_column(String(512), nullable=False)
    # URL de snapshot HTTP (opcional — algunos NVR lo proveen)
    snapshot_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    status: Mapped[CameraStatus] = mapped_column(
        Enum(CameraStatus, name="camerastatus"),
        nullable=False,
        default=CameraStatus.INACTIVE,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # FPS objetivo para el pipeline de inferencia (overrides la config global)
    target_fps: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relaciones (definidas en fases posteriores)
    zones: Mapped[list["Zone"]] = relationship(  # noqa: F821
        "Zone", back_populates="camera", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(  # noqa: F821
        "Event", back_populates="camera"
    )

    def __repr__(self) -> str:
        return f"<Camera id={self.id} name={self.name!r} status={self.status}>"
