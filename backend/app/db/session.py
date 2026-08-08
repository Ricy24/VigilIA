"""
Sesión de base de datos SQLAlchemy.

Provee:
  - engine:       motor SQLAlchemy (síncrono, para Alembic y health checks)
  - SessionLocal: fábrica de sesiones síncronas
  - get_db():     dependencia FastAPI que provee una sesión por request
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Motor síncrono — usado por Alembic y el health check
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,        # verifica la conexión antes de usarla
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,       # loguea SQL en modo debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia FastAPI — inyecta una sesión DB en los endpoints.

    Uso:
        @router.get("/cameras")
        def list_cameras(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
