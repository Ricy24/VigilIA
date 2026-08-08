"""
VigilIA Inference Pipeline — Entry Point

Punto de entrada del pipeline de visión artificial.
En la Fase 0 solo verifica la configuración y los imports.
El pipeline completo se implementa en la Fase 2.
"""

import sys
import logging

from pipeline.config import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("vigilia.inference")


def main() -> None:
    logger.info("🔍 VigilIA Inference Pipeline iniciando")
    logger.info(f"Entorno: {settings.ENVIRONMENT}")
    logger.info(f"Backend URL: {settings.BACKEND_URL}")
    logger.info(f"Redis URL: {settings.REDIS_URL}")
    logger.info(f"Device: {settings.DEVICE}")
    logger.info("Pipeline base OK — implementación completa en Fase 2")


if __name__ == "__main__":
    main()
