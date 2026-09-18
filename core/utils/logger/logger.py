from __future__ import annotations

import logging

LOGGER_NAME: str = "itac-competition"

def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
