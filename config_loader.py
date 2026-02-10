import json
import os
import sys

APP_NAME = "Startup Notifier"


def get_primary_config_path():
    if sys.platform == "win32":
        return os.path.join(
            os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
            APP_NAME,
            "config.json"
        )
    raise RuntimeError("Unsupported OS")


def get_fallback_config_path():
    return os.path.join(os.getcwd(), "config.json")


def load_config():
    primary_path = get_primary_config_path()
    fallback_path = get_fallback_config_path()

    config_path = None

    if os.path.exists(primary_path):
        config_path = primary_path
    elif os.path.exists(fallback_path):
        config_path = fallback_path
    else:
        raise FileNotFoundError(
            f"Config file not found. Checked:\n"
            f"- {primary_path}\n"
            f"- {fallback_path}"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
