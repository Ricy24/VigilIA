"""
Schemas Pydantic — Zone
"""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from app.db.models.zone import ZoneType


class Point(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)


class ZoneBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    zone_type: ZoneType = ZoneType.EXCLUSION
    polygon: List[Point] = Field(..., min_length=3)
    is_active: bool = True
    required_ppe: Optional[List[str]] = None
    min_duration_seconds: int = Field(5, ge=0)


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    zone_type: Optional[ZoneType] = None
    polygon: Optional[List[Point]] = Field(None, min_length=3)
    is_active: Optional[bool] = None
    required_ppe: Optional[List[str]] = None
    min_duration_seconds: Optional[int] = Field(None, ge=0)


class ZoneResponse(ZoneBase):
    id: int
    camera_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
