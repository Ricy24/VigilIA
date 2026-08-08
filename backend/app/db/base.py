"""Base declarativa de SQLAlchemy para todos los modelos ORM."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos de VigilIA.

    Todos los modelos deben heredar de esta clase:
        class Camera(Base):
            __tablename__ = "cameras"
            ...
    """
    pass
