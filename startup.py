# startup.py

import winreg
import os
from logger import setup_logger

logger = setup_logger()

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_REG_NAME = "StartupNotifier"


def add_to_startup(exe_path: str):
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            RUN_KEY_PATH,
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, APP_REG_NAME, 0, winreg.REG_SZ, exe_path)

        logger.info("Application added to Windows startup")
    except Exception as e:
        logger.error(f"Failed to add to startup: {e}")


def remove_from_startup():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            RUN_KEY_PATH,
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, APP_REG_NAME)

        logger.info("Application removed from Windows startup")
    except FileNotFoundError:
        logger.warning("Startup registry entry not found")
    except Exception as e:
        logger.error(f"Failed to remove from startup: {e}")
