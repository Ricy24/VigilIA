"""
Schemas Pydantic — User

Separa explícitamente los schemas de:
  - Base: campos comunes (lectura)
  - Create: campos para crear (incluye contraseña)
  - Update: campos opcionales para actualizar
  - Response: lo que se devuelve al cliente (nunca incluye hashed_password)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.db.models.user import UserRole


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    role: UserRole = UserRole.SUPERVISOR
    is_active: bool = True


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


# ---------------------------------------------------------------------------
# Update (todos opcionales)
# ---------------------------------------------------------------------------
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)


# ---------------------------------------------------------------------------
# Response (salida al cliente — sin contraseña)
# ---------------------------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
