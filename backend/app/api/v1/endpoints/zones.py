"""
Endpoints para la gestión de Zonas de Seguridad.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin, get_current_user, get_db
from app.db.models.camera import Camera
from app.db.models.zone import Zone
from app.db.models.user import User
from app.schemas.zone import ZoneCreate, ZoneResponse, ZoneUpdate

router = APIRouter()


@router.get("/cameras/{camera_id}/zones", response_model=List[ZoneResponse])
def read_camera_zones(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Obtener lista de zonas asociadas a una cámara.
    """
    # Verificar si la cámara existe
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")

    zones = db.query(Zone).filter(Zone.camera_id == camera_id).all()
    return zones


@router.post(
    "/cameras/{camera_id}/zones",
    response_model=ZoneResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_zone(
    *,
    db: Session = Depends(get_db),
    camera_id: int,
    zone_in: ZoneCreate,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Crear una nueva zona para una cámara (Solo Administradores).
    """
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")

    zone_data = zone_in.model_dump()
    # Pydantic nos entregará un listado de dicts para el poligono, SQLAlchemy JSON lo recibe bien.
    
    zone = Zone(**zone_data, camera_id=camera_id)
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.get("/zones/{zone_id}", response_model=ZoneResponse)
def read_zone(
    zone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Obtener el detalle de una zona.
    """
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zone


@router.patch("/zones/{zone_id}", response_model=ZoneResponse)
def update_zone(
    *,
    db: Session = Depends(get_db),
    zone_id: int,
    zone_in: ZoneUpdate,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Actualizar la configuración o polígono de una zona (Solo Administradores).
    """
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    update_data = zone_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(zone, field, value)

    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/zones/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(
    *,
    db: Session = Depends(get_db),
    zone_id: int,
    current_user: User = Depends(get_current_active_admin),
) -> None:
    """
    Eliminar una zona (Solo Administradores).
    """
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    db.delete(zone)
    db.commit()
