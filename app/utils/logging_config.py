# uncomment all the code when u want log file
import logging
import logging.config
from pathlib import Path

# LOG_DIR = Path("logs")
# LOG_DIR.mkdir(exist_ok=True)

# LOG_FILE = LOG_DIR / "app.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        },
        # "detailed": {
        #     "format": "%(asctime)s | %(levelname)s | %(name)s | [%(filename)s:%(lineno)d] %(message)s"
        # }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        # "file": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": str(LOG_FILE),
        #     "maxBytes": 5 * 1024 * 1024,  # 5MB
        #     "backupCount": 5,
        #     "formatter": "detailed",
        #     "level": "INFO",
        # },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },

    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}
