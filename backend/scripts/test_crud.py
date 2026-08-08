"""
Prueba rápida de integración para CRUD y Auth.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.api.deps import get_db

client = TestClient(app)

def test_flow():
    print("1. Intentando Login con admin...")
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@vigilia.com", "password": "admin1234"}
    )
    assert response.status_code == 200, f"Login falló: {response.text}"
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ Login exitoso. Token obtenido.")

    print("2. Creando Cámara...")
    import random
    cam_name = f"Camara Entrada Principal {random.randint(1000, 9999)}"
    cam_data = {
        "name": cam_name,
        "location": "Entrada Norte",
        "site": "Planta 1",
        "rtsp_url": "rtsp://admin:pass@192.168.1.100:554/stream1"
    }
    response = client.post("/api/v1/cameras/", json=cam_data, headers=headers)
    assert response.status_code == 201, f"Crear cámara falló: {response.text}"
    cam_id = response.json()["id"]
    print(f"   ✅ Cámara creada con ID: {cam_id}")

    print("3. Creando Zona para la Cámara...")
    zone_data = {
        "name": "Zona Exclusión Puerta",
        "zone_type": "exclusion",
        "polygon": [
            {"x": 0.1, "y": 0.1},
            {"x": 0.9, "y": 0.1},
            {"x": 0.9, "y": 0.9},
            {"x": 0.1, "y": 0.9}
        ]
    }
    response = client.post(f"/api/v1/cameras/{cam_id}/zones", json=zone_data, headers=headers)
    assert response.status_code == 201, f"Crear zona falló: {response.text}"
    zone_id = response.json()["id"]
    print(f"   ✅ Zona creada con ID: {zone_id}")

    print("4. Listando zonas de la cámara...")
    response = client.get(f"/api/v1/cameras/{cam_id}/zones", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    print(f"   ✅ Zonas listadas correctamente: {len(response.json())} zonas encontradas.")

if __name__ == "__main__":
    test_flow()
    print("TODAS LAS PRUEBAS PASARON EXITOSAMENTE! 🚀")
