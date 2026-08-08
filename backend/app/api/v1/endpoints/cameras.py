"""
Endpoints para la gestión de Cámaras.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin, get_current_user, get_db
from app.db.models.camera import Camera
from app.db.models.user import User
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate

router = APIRouter()


@router.get("/", response_model=List[CameraResponse])
def read_cameras(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Obtener lista de cámaras registradas.
    Cualquier usuario autenticado puede verlas (supervisor, hse, admin).
    """
    cameras = db.query(Camera).offset(skip).limit(limit).all()
    return cameras


@router.post("/", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(
    *,
    db: Session = Depends(get_db),
    camera_in: CameraCreate,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Registrar una nueva cámara (Solo Administradores).
    """
    # Validar si ya existe una cámara con ese nombre (opcional, pero buena práctica)
    if db.query(Camera).filter(Camera.name == camera_in.name).first():
        raise HTTPException(
            status_code=400,
            detail="Ya existe una cámara con ese nombre.",
        )

    camera = Camera(**camera_in.model_dump())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


@router.get("/{camera_id}", response_model=CameraResponse)
def read_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Obtener detalle de una cámara específica.
    """
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return camera


@router.patch("/{camera_id}", response_model=CameraResponse)
def update_camera(
    *,
    db: Session = Depends(get_db),
    camera_id: int,
    camera_in: CameraUpdate,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Actualizar configuración de una cámara (Solo Administradores).
    """
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")

    update_data = camera_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(camera, field, value)

    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(
    *,
    db: Session = Depends(get_db),
    camera_id: int,
    current_user: User = Depends(get_current_active_admin),
) -> None:
    """
    Eliminar una cámara del sistema (Solo Administradores).
    """
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    
    db.delete(camera)
    db.commit()
