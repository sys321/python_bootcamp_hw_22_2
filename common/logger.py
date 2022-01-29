import os
import logging
import logging.config

cfg = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": "%(asctime)s - %(ms)s \ %(method)s: %(message)s"
        }
    },
    "handlers": {
        "handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename":
                os.path.abspath(
                    os.path.join(
                        os.path.join(
                            os.path.join(
                                os.path.dirname(__file__), ".."), "logs"), "app.log")),
            "mode": "a"
        }
    },
    "loggers": {
        "logger": {
            "handlers": ["handler"],
            "level": "DEBUG"
        }
    }
}

logging.config.dictConfig(cfg)
logger = logging.getLogger("logger")
