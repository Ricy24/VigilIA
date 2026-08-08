"""
Modelo ORM: Zone

Representa una zona de interés delimitada en el campo de visión de una cámara.
El polígono se almacena como JSON: lista de puntos [{"x": 0.1, "y": 0.2}, ...]
con coordenadas normalizadas (0.0 a 1.0 relativas al ancho/alto de la imagen).

Tipos de zona:
  - exclusion   → zona de exclusión (no debe entrar nadie sin autorización)
  - ppe_required → zona donde se exige EPP específico
  - monitoring  → zona de monitoreo general (sin regla específica activa)
"""

import enum
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ZoneType(str, enum.Enum):
    EXCLUSION = "exclusion"
    PPE_REQUIRED = "ppe_required"
    MONITORING = "monitoring"


class Zone(Base):
    __tablename__ = "zones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    camera_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    zone_type: Mapped[ZoneType] = mapped_column(
        Enum(ZoneType, name="zonetype"), nullable=False, default=ZoneType.EXCLUSION
    )

    # Polígono como lista de puntos normalizados: [{"x": 0.1, "y": 0.2}, ...]
    # Coordenadas relativas a la imagen (0.0 - 1.0)
    polygon: Mapped[list[Any]] = mapped_column(JSON, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Para zonas PPE_REQUIRED: qué EPP se exige
    # Ej: ["helmet", "vest", "gloves"]
    required_ppe: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Tiempo mínimo (segundos) antes de generar alerta (evita falsos positivos por tránsito)
    min_duration_seconds: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

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

    # Relaciones
    camera: Mapped["Camera"] = relationship("Camera", back_populates="zones")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Zone id={self.id} name={self.name!r} type={self.zone_type}>"
