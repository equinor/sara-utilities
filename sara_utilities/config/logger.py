from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s - %(asctime)s - %(name)s -  %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "azure.core": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def setup_logger() -> None:
    dictConfig(LOGGING_CONFIG)
