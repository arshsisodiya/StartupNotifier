# logger.py

import logging
import os
from logging.handlers import RotatingFileHandler
import sys

APP_NAME = "StartupNotifier"


def get_app_data_dir():
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(base, APP_NAME)
    return os.path.join(os.path.expanduser("~"), f".{APP_NAME.lower()}")


def setup_logger():
    log_dir = get_app_data_dir()
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    logger = logging.getLogger("startup_notifier")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
