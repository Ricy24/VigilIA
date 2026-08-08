"""
VigilIA — Configuración centralizada del backend.

Todas las variables de entorno se leen desde el archivo .env
mediante pydantic-settings. Nunca se hardcodean valores sensibles.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación leída desde variables de entorno.
    Los valores por defecto son seguros para desarrollo local.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # General
    # -------------------------------------------------------------------------
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "VigilIA"
    VERSION: str = "0.1.0"

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------
    API_V1_STR: str = "/api/v1"

    # -------------------------------------------------------------------------
    # CORS — en producción restringir a los dominios reales
    # -------------------------------------------------------------------------
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # -------------------------------------------------------------------------
    # Base de datos (PostgreSQL)
    # -------------------------------------------------------------------------
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "vigilia"
    POSTGRES_PASSWORD: str = "vigilia_dev_pass"
    POSTGRES_DB: str = "vigilia"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # -------------------------------------------------------------------------
    # Autenticación JWT
    # -------------------------------------------------------------------------
    SECRET_KEY: str = "CAMBIA_ESTO_EN_PRODUCCION_usa_openssl_rand_hex_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -------------------------------------------------------------------------
    # Inference Service
    # -------------------------------------------------------------------------
    INFERENCE_SERVICE_URL: str = "http://localhost:8001"

    # -------------------------------------------------------------------------
    # LLM (Fase 6)
    # -------------------------------------------------------------------------
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"


@lru_cache
def get_settings() -> Settings:
    """Singleton de configuración — cachea la instancia para toda la aplicación."""
    return Settings()


# Instancia global para importar directamente en otros módulos
settings = get_settings()
