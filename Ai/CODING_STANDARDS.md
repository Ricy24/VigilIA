# CODING_STANDARDS.md — Estándares de Código VigilIA

---

## Python (Backend + Inference)

### Estilo general
- Seguir **PEP 8** estrictamente
- Líneas máximo **100 caracteres**
- Usar **type hints** en todas las funciones y métodos públicos
- **Docstrings** en todos los módulos, clases y funciones públicas (formato Google o NumPy)

### Imports
```python
# Orden: stdlib → third-party → local (separados por línea en blanco)
import os
import time
from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
```

### Naming
| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Variables/funciones | `snake_case` | `get_camera_by_id` |
| Clases | `PascalCase` | `CameraService` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RECONNECT_ATTEMPTS` |
| Módulos | `snake_case` | `yolo_detector.py` |
| Archivos de test | `test_*.py` | `test_detection.py` |

### FastAPI patterns
```python
# ✅ Correcto: dependencias inyectadas, tipado, response model declarado
@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CameraResponse:
    """Retorna los detalles de una cámara por ID."""
    camera = camera_service.get_by_id(db, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return camera

# ❌ Incorrecto: sin tipado, sin response model, lógica de negocio en el endpoint
@router.get("/{id}")
def get_cam(id, db = Depends(get_db)):
    return db.query(Camera).filter(Camera.id == id).first()
```

### Manejo de errores
```python
# Siempre usar HTTPException con mensajes en español (es la lengua del sistema)
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Cámara no encontrada",
)
```

### Tests (pytest)
```python
# Nombrar tests descriptivamente
def test_create_camera_returns_201_with_valid_data():
    ...

def test_create_camera_returns_422_without_rtsp_url():
    ...
```

---

## TypeScript / React (Frontend)

### Estilo general
- **TypeScript strict mode** — no usar `any` salvo casos excepcionales justificados en comentario
- Componentes React en `PascalCase.tsx`
- Hooks en `use*.ts`
- Servicios en `*.service.ts`

### Interfaces sobre Types (para objetos)
```typescript
// ✅ Preferir interface para shapes de objetos
interface Camera {
  id: number
  name: string
  rtspUrl: string
  status: 'active' | 'inactive' | 'error'
}

// ✅ Type para unions y primitivos
type AlertSeverity = 'low' | 'medium' | 'high' | 'critical'
```

### Componentes React
```tsx
// ✅ Función con props tipadas explícitamente
interface AlertCardProps {
  alert: Alert
  onAcknowledge: (id: number) => void
}

export function AlertCard({ alert, onAcknowledge }: AlertCardProps) {
  return (
    <div className="alert-card" data-severity={alert.severity}>
      ...
    </div>
  )
}
```

### CSS: Variables del Design System
```css
/* ✅ Usar variables CSS del design system */
.btn-primary {
  background: var(--color-brand-500);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

/* ❌ No hardcodear valores */
.btn-primary {
  background: #3b82f6;
  border-radius: 8px;
}
```

---

## Git

### Mensajes de commit
```
feat: agregar endpoint POST /cameras
fix: corregir reconexión RTSP ante timeout
refactor: separar lógica de tracking en módulo propio
docs: actualizar ROADMAP con estado Fase 1
test: agregar tests para motor de reglas EPP
chore: actualizar dependencias requirements.txt
```

### Ramas
```
main          ← código estable, siempre funcional
dev           ← integración de features
feat/nombre   ← features nuevas
fix/nombre    ← correcciones
```

---

## Seguridad (obligatorio)

- **Nunca** hardcodear secrets, API keys o contraseñas en el código
- **Nunca** subir `.env` al repositorio
- Usar `settings.SECRET_KEY` etc., siempre desde la configuración
- Validar y sanitizar toda entrada del usuario antes de procesarla
- En rutas protegidas, siempre usar `Depends(get_current_user)`
