# telegram_client.py

import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, REQUEST_TIMEOUT
from logger import setup_logger

logger = setup_logger()


class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

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
                logger.info("Telegram message sent successfully")
                return True
            except requests.RequestException as e:
                logger.warning(f"Telegram attempt {attempt} failed: {e}")
                time.sleep(delay)

        logger.error("All Telegram send attempts failed")
        return False
