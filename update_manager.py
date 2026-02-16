import requests
import os
import threading
import subprocess
from packaging import version
from pathlib import Path
import tkinter as tk
from tkinter import ttk

API_URL = "https://api.github.com/repos/arshsisodiya/StartupNotifier/releases/latest"
INSTALLER_NAME_PREFIX = "StartupNotifierSetup"


def get_current_version():
    # Read version dynamically from file
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"


class UpdateManager:

    def __init__(self, silent=False, logger=None):
        self.silent = silent
        self.logger = logger
        self.root = None
        self.progress = None
        self.status_label = None
        self.current_version = get_current_version()


    # ---------------- UI ---------------- #

    def _create_ui(self):
        self.root = tk.Tk()
        self.root.title("Updating Startup Notifier")
        self.root.geometry("400x120")
        self.root.resizable(False, False)

        self.status_label = tk.Label(self.root, text="Checking for updates...")
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=350)
        self.progress.pack(pady=5)

        self.root.update()

    def _update_progress(self, percent):
        if not self.silent and self.progress:
            self.root.after(0, lambda: self.progress.config(value=percent))

    def _update_status(self, message):
        if not self.silent and self.status_label:
            self.root.after(0, lambda: self.status_label.config(text=message))

    # ---------------- Core ---------------- #

    def start(self):
        thread = threading.Thread(target=self._run_update, daemon=True)
        thread.start()

        if not self.silent:
            self._create_ui()
            self.root.mainloop()

    def _run_update(self):
        update_info = self._check_for_update()

        if not update_info:
            if not self.silent and self.root:
                self._update_status("You are using the latest version.")
                self.root.after(2000, self.root.destroy)
            return

        self._download_and_install(update_info["url"])

    def _check_for_update(self):
        try:
            self._update_status("Checking GitHub for latest release...")

            headers = {"User-Agent": "StartupNotifier-Updater"}
            response = requests.get(API_URL, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            latest_version = data["tag_name"].lstrip("v")

            if self.logger:
                self.logger.info(
                    f"Current version: {self.current_version} | "
                    f"Latest version on GitHub: {latest_version}"
                )

            if version.parse(latest_version) > version.parse(self.current_version):

                if self.logger:
                    self.logger.info("Update available.")

                for asset in data["assets"]:
                    if asset["name"].startswith(INSTALLER_NAME_PREFIX):
                        return {
                            "version": latest_version,
                            "url": asset["browser_download_url"]
                        }

                if self.logger:
                    self.logger.warning("Update detected but no matching installer asset found.")

            else:
                if self.logger:
                    self.logger.info("No update available. Application is up to date.")

            return None

        except Exception as e:
            if self.logger:
                self.logger.error(f"Update check failed: {e}")
            return None

    def _download_and_install(self, url):
        try:
            self._update_status("Downloading update...")

            headers = {"User-Agent": "StartupNotifier-Updater"}
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192

            temp_path = Path(os.getenv("TEMP")) / "StartupNotifierUpdate.exe"

            with open(temp_path, "wb") as file:
                downloaded = 0
                for chunk in response.iter_content(block_size):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = int(downloaded * 100 / total_size)
                            self._update_progress(percent)

            self._update_status("Installing update...")

            subprocess.Popen(
                [str(temp_path), "/verysilent", "/norestart"],
                shell=True
            )

            os._exit(0)

        except Exception as e:
            print("Update failed:", e)
            if not self.silent and self.root:
                self._update_status("Update failed.")
                self.root.after(3000, self.root.destroy)
