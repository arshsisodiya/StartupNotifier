import win32gui
import win32process
import psutil
import datetime
import csv
import time
import os
from url_sniffer import get_browser_url
from pynput import mouse, keyboard
from storage import get_data_dir
APP_NAME = "Startup Notifier"
# 🚀 Configuration for Idle Detection
IDLE_THRESHOLD = 120  # 2 minutes in seconds


# --- Input Tracking Logic ---
class InputCounter:
    def __init__(self):
        self.kb_count = 0
        self.mouse_count = 0
        self.last_input_time = time.time()  # 🚀 Track last physical activity

        # Start listeners in background threads
        self.kb_listener = keyboard.Listener(on_press=self._on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self._on_mouse_click)

        self.kb_listener.start()
        self.mouse_listener.start()

    def _on_key_press(self, key):
        self.kb_count += 1
        self.last_input_time = time.time()  # 🚀 Reset idle clock on key press

    def _on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_count += 1
            self.last_input_time = time.time()  # 🚀 Reset idle clock on mouse click

    def get_idle_time(self):
        """Returns how many seconds since the last input."""
        return time.time() - self.last_input_time

    def get_and_reset(self):
        """Returns current counts and resets them for the next window session."""
        counts = (self.kb_count, self.mouse_count)
        self.kb_count = 0
        self.mouse_count = 0
        return counts


# Initialize the global counter
input_tracker = InputCounter()


def is_media_active(info):
    """🚀 Checks if the current window is a media player or video site."""
    if not info: return False

    app = info["app_name"].lower()
    title = info["title"].lower()

    # Dedicated media apps
    media_apps = ["vlc.exe", "mpc-hc.exe", "spotify.exe", "netflix.exe"]
    # Browser keywords for video sites
    web_media = ["youtube", "netflix", "prime video", "hotstar", "twitch", "vimeo"]

    if any(m in app for m in media_apps):
        return True
    if any(w in title for w in web_media):
        return True
    return False


def get_daily_log_file():
    """Generates a filename based on the current date."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"activity_log_{date_str}.csv"
    return os.path.join(get_data_dir(), filename)


def format_duration(seconds):
    """Formats raw seconds into 'X Minutes Y Seconds' or 'X Seconds'."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} Seconds"

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if remaining_seconds == 0:
        return f"{minutes} Minutes"
    else:
        return f"{minutes} Minutes {remaining_seconds} Seconds"


def ensure_log_file(file_path):
    """Creates the directory and file with headers if they don't exist."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Timestamp", "Application", "PID", "Window Title", "URL", "Duration", "Keystrokes", "Clicks"])


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

        url = "N/A"
        if any(b in app_name.lower() for b in ["chrome", "msedge", "brave"]):
            url = get_browser_url()

        return {"app_name": app_name, "pid": pid, "title": title.strip(), "url": url}
    except Exception:
        return None


def start_logging():
    """Main loop: Detects changes and logs formatted duration with idle-aware tracking."""
    last_info = None
    start_time = time.time()
    total_idle_deduction = 0  # 🚀 Accumulates paused time

    while True:
        try:
            current_log_file = get_daily_log_file()
            ensure_log_file(current_log_file)

            info = get_active_window_info()
            idle_seconds = input_tracker.get_idle_time()

            # 🚀 Idle if threshold exceeded AND it's not a media app
            is_idle = idle_seconds > IDLE_THRESHOLD and not is_media_active(info)

            if info:
                if last_info is None:
                    last_info = info
                    start_time = time.time()
                    input_tracker.get_and_reset()
                    total_idle_deduction = 0

                elif (info["app_name"] != last_info["app_name"] or
                      info["pid"] != last_info["pid"] or
                      info["title"] != last_info["title"] or
                      info["url"] != last_info["url"]):

                    # 🚀 Final duration = Total time - Time spent idling
                    raw_seconds = (time.time() - start_time) - total_idle_deduction
                    if raw_seconds < 0: raw_seconds = 0

                    readable_duration = format_duration(raw_seconds)
                    keys, clicks = input_tracker.get_and_reset()
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Log only if there was active time
                    if raw_seconds > 0:
                        with open(current_log_file, "a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                timestamp, last_info["app_name"], last_info["pid"],
                                last_info["title"], last_info["url"], readable_duration,
                                keys, clicks
                            ])

                    last_info = info
                    start_time = time.time()
                    total_idle_deduction = 0

                # 🚀 If user is currently idle, subtract this second from active time
                if is_idle:
                    total_idle_deduction += 1

            time.sleep(1)
        except Exception:
            time.sleep(1)


if __name__ == "__main__":
    start_logging()