"""
VigilIA Inference Pipeline — Configuración.

Lee variables de entorno desde .env en la raíz del servicio.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class InferenceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Backend API
    BACKEND_URL: str = "http://localhost:8000"
    BACKEND_API_KEY: str = ""  # Para autenticar eventos al backend (Fase 4)

    # Redis (cola de frames)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # YOLO / Modelo
    YOLO_MODEL_PATH: str = "yolo11n.pt"   # Nano — más rápido para dev/pruebas
    YOLO_CONFIDENCE_THRESHOLD: float = 0.5
    YOLO_IOU_THRESHOLD: float = 0.45

    # Inferencia
    DEVICE: str = "cpu"           # "cpu" | "cuda" | "cuda:0"
    TARGET_FPS: int = 10          # FPS objetivo del pipeline (no el nativo de la cámara)
    FRAME_SKIP: int = 3           # Procesar 1 de cada N frames del stream nativo

    # Ingesta
    RTSP_RECONNECT_DELAY_SECONDS: int = 5


@lru_cache
def get_settings() -> InferenceSettings:
    return InferenceSettings()


settings = get_settings()
