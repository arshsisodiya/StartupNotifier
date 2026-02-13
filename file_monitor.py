import time
import os
import csv
import datetime
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

APP_NAME = "Startup Notifier"
BASE_DIR = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), APP_NAME)

def get_daily_log_file():
    """Generates filename: system_file_activity_YYYY-MM-DD.csv"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(BASE_DIR, f"system_file_activity_{date_str}.csv")

def get_local_drives():
    """Detects all mounted fixed drives (C:\, D:\, etc.)"""
    return [p.mountpoint for p in psutil.disk_partitions() if 'fixed' in p.opts]

# Folders to ignore to prevent infinite loops and system noise
IGNORE_KEYWORDS = ["$Recycle.Bin", "AppData", "Temp", "ProgramData", "Windows", "System Volume Information", "Program Files", APP_NAME]

class AdvancedActivityHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_logged = {}

    def should_ignore(self, path):
        # 🚀 CRITICAL: Ignore the log folder itself
        if path.startswith(BASE_DIR): return True
        return any(k.lower() in path.lower() for k in IGNORE_KEYWORDS)

    def log_event(self, action, path):
        now = time.time()
        # Throttle logic to prevent double-logging rapid events
        if path in self.last_logged and now - self.last_logged[path] < 1: return
        self.last_logged[path] = now

        log_path = get_daily_log_file()
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        if not os.path.exists(log_path):
            with open(log_path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Timestamp", "Action", "File Path"])

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(log_path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([timestamp, action, path])
        except Exception: pass

    def on_created(self, event):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.log_event("CREATED/DOWNLOADED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.log_event("MODIFIED", event.src_path)

    def on_moved(self, event):
        # 🚀 This captures renames and moves across folders
        if not event.is_directory:
            if not self.should_ignore(event.src_path) or not self.should_ignore(event.dest_path):
                self.log_event("MOVED/RENAMED", f"{event.src_path} -> {event.dest_path}")

    def on_deleted(self, event):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.log_event("DELETED", event.src_path)

def start_file_watchdog():
    """Initializes multi-drive monitoring."""
    observer = Observer()
    event_handler = AdvancedActivityHandler()
    for drive in get_local_drives():
        try:
            observer.schedule(event_handler, drive, recursive=True)
            print(f"Monitoring: {drive}")
        except Exception: pass
    observer.start()
    try:
        while True: time.sleep(10)
    except Exception: observer.stop()
    observer.join()