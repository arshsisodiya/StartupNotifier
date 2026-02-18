# network.py

import socket
import time
from src.utils.logger import setup_logger

logger = setup_logger()


def wait_for_internet(timeout=60, interval=5) -> bool:
    """
    Wait until internet is available or timeout expires.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            logger.info("Internet connection detected")
            return True
        except OSError:
            logger.info("Waiting for internet...")
            time.sleep(interval)

    logger.error("Internet not available after timeout")
    return False
