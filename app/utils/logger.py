import logging
import logging.config
from app.utils.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str = "app"):
    return logging.getLogger(name)
