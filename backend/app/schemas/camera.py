"""
Schemas Pydantic — Camera
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, AnyHttpUrl

from app.db.models.camera import CameraStatus


class CameraBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    location: str = Field(..., min_length=2, max_length=255)
    site: str = Field(..., min_length=2, max_length=255)
    rtsp_url: str = Field(..., max_length=512)
    snapshot_url: Optional[str] = Field(None, max_length=512)
    is_active: bool = True
    description: Optional[str] = None
    target_fps: int = Field(10, ge=1, le=60)


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    site: Optional[str] = Field(None, min_length=2, max_length=255)
    rtsp_url: Optional[str] = Field(None, max_length=512)
    snapshot_url: Optional[str] = Field(None, max_length=512)
    is_active: Optional[bool] = None
    description: Optional[str] = None
    target_fps: Optional[int] = Field(None, ge=1, le=60)
    status: Optional[CameraStatus] = None


class CameraResponse(CameraBase):
    id: int
    status: CameraStatus
    created_at: datetime
    updated_at: datetime
    last_seen_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
