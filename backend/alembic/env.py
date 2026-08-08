"""
Alembic env.py — Configuración del entorno de migraciones.

Integra Alembic con:
  - La configuración centralizada de VigilIA (app.core.config)
  - Los modelos ORM (app.db.models) para autogenerar migraciones
  - Soporte para migraciones online (con DB) y offline (con SQL script)
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# ---------------------------------------------------------------------------
# Importar config y modelos de VigilIA
# ---------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.base import Base
import app.db.models  # noqa: F401 — registra todos los modelos en Base.metadata

# ---------------------------------------------------------------------------
# Configuración de Alembic
# ---------------------------------------------------------------------------
config = context.config

# Sobreescribir la URL de BD con la de nuestra configuración (ignora alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLAlchemy con todos los modelos cargados
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Modo offline: genera el SQL sin conectarse a la BD.
    Útil para generar scripts SQL para revisión antes de aplicar.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Modo online: conecta a la BD y aplica las migraciones directamente.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
