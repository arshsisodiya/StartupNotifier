import win32gui
import win32process
import psutil
import datetime
import csv
import time
import os
from url_sniffer import get_browser_url  # 🚀 Assumes your sniffer script is in the same folder

APP_NAME = "Startup Notifier"
# Stores logs in C:\ProgramData\Startup Notifier
BASE_DIR = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), APP_NAME)


def get_daily_log_file():
    """Generates a filename based on the current date."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"activity_log_{date_str}.csv"
    return os.path.join(BASE_DIR, filename)


def ensure_log_file(file_path):
    """Creates the directory and file with headers if they don't exist."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Application", "PID", "Window Title", "URL"])


def get_active_window_info():
    """Captures foreground window details and sniffs browser URLs."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0: return None
        title = win32gui.GetWindowText(hwnd)
        if not title: return None

        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        app_name = process.name()

        # Sniff URL if a common browser is detected
        url = "N/A"
        if any(b in app_name.lower() for b in ["chrome", "msedge", "brave"]):
            url = get_browser_url()

        return {"app_name": app_name, "pid": pid, "title": title.strip(), "url": url}
    except Exception:
        return None


def start_logging():
    """Main loop: Detects changes and writes to the daily CSV."""
    last_entry = None
    while True:
        try:
            current_log_file = get_daily_log_file()
            ensure_log_file(current_log_file)

            info = get_active_window_info()
            if info:
                current_entry = (info["app_name"], info["pid"], info["title"], info["url"])
                if current_entry != last_entry:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(current_log_file, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, info["app_name"], info["pid"], info["title"], info["url"]])
                    last_entry = current_entry
            time.sleep(1)  # Frequency of checks
        except Exception:
            time.sleep(1)