"""PISA-standard `logging.basicConfig` so every wrapper emits the same
format and level. Idempotent — safe to call from multiple entry
points; later calls do nothing once a root handler is configured.
"""

import logging

DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(level: int = logging.INFO, format: str = DEFAULT_FORMAT) -> None:
    logging.basicConfig(level=level, format=format, handlers=[logging.StreamHandler()])
