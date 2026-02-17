# config_loader.py

import os
import requests
import tkinter as tk
from tkinter import messagebox
from secure_config import encrypt_data, decrypt_data
from storage import get_config_path


# ===============================
# TELEGRAM VALIDATION
# ===============================

def validate_telegram(bot_token, chat_id):
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getMe",
            timeout=10
        )
        if not r.ok:
            return False, "Invalid Bot Token"

        r2 = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getChat",
            params={"chat_id": chat_id},
            timeout=10
        )
        if not r2.ok:
            return False, "Invalid Chat ID"

        return True, "OK"

    except Exception as e:
        return False, str(e)


def is_valid_config(config):
    try:
        bot = config["telegram"]["bot_token"]
        chat = config["telegram"]["chat_id"]
        valid, _ = validate_telegram(bot, chat)
        return valid
    except Exception:
        return False


# ===============================
# CONFIG CREATION
# ===============================

def create_config(bot_token, chat_id):
    config_path = get_config_path()

    config_data = {
        "ui_mode": "normal",
        "startup_delay": 15,
        "logging": {"level": "info"},
        "telegram": {
            "bot_token": bot_token,
            "chat_id": chat_id
        }
    }

    encrypted_blob = encrypt_data(config_data)

    with open(config_path, "wb") as f:
        f.write(encrypted_blob)

    return config_data


# ===============================
# LOAD CONFIG
# ===============================

def load_config():
    config_path = get_config_path()

    # 1️⃣ If encrypted config exists → decrypt
    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                encrypted_blob = f.read()

            config = decrypt_data(encrypted_blob)

            if is_valid_config(config):
                return config
            else:
                os.remove(config_path)

        except Exception:
            # corrupted config
            os.remove(config_path)

    # 2️⃣ Prompt user for setup
    bot_token, chat_id = prompt_for_config()
    return create_config(bot_token, chat_id)


# ===============================
# UI SETUP PROMPT
# ===============================

def prompt_for_config():
    result = {}

    def toggle_password():
        if bot_entry.cget("show") == "*":
            bot_entry.config(show="")
            toggle_btn.config(text="Hide")
        else:
            bot_entry.config(show="*")
            toggle_btn.config(text="Show")

    def on_validate():
        bot = bot_entry.get().strip()
        chat = chat_entry.get().strip()

        if not bot or not chat:
            messagebox.showerror("Error", "All fields are required.")
            return

        status_label.config(text="Validating...", fg="#FFC107")
        root.update()

        valid, msg = validate_telegram(bot, chat)

        if valid:
            status_label.config(text="✔ Telegram validated", fg="#4CAF50")
            save_button.config(state="normal")
            result["bot"] = bot
            result["chat"] = chat
        else:
            status_label.config(text=f"✖ {msg}", fg="#F44336")
            save_button.config(state="disabled")

    def on_save():
        root.destroy()

    root = tk.Tk()
    root.title("Startup Notifier Setup")
    root.geometry("440x300")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")

    tk.Label(
        root,
        text="Telegram Configuration",
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(15, 10))

    # Bot Token
    tk.Label(root, text="Bot Token:", bg="#1e1e1e", fg="white").pack(anchor="w", padx=30)

    bot_frame = tk.Frame(root, bg="#1e1e1e")
    bot_frame.pack(padx=30, fill="x")

    bot_entry = tk.Entry(
        bot_frame,
        bg="#2d2d2d",
        fg="white",
        insertbackground="white",
        show="*"
    )
    bot_entry.pack(side="left", fill="x", expand=True)

    toggle_btn = tk.Button(
        bot_frame,
        text="Show",
        bg="#444",
        fg="white",
        width=6,
        command=toggle_password
    )
    toggle_btn.pack(side="right", padx=(5, 0))

    # Chat ID
    tk.Label(root, text="Chat ID:", bg="#1e1e1e", fg="white").pack(anchor="w", padx=30, pady=(15, 0))

    chat_entry = tk.Entry(
        root,
        bg="#2d2d2d",
        fg="white",
        insertbackground="white"
    )
    chat_entry.pack(padx=30, fill="x", pady=(0, 15))

    status_label = tk.Label(root, text="", bg="#1e1e1e", fg="white")
    status_label.pack()

    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=20)

    validate_button = tk.Button(
        button_frame,
        text="Validate",
        bg="#0078D7",
        fg="white",
        width=12,
        command=on_validate
    )
    validate_button.grid(row=0, column=0, padx=5)

    save_button = tk.Button(
        button_frame,
        text="Save",
        bg="#4CAF50",
        fg="white",
        width=12,
        state="disabled",
        command=on_save
    )
    save_button.grid(row=0, column=1, padx=5)

    root.mainloop()

    if "bot" not in result:
        raise RuntimeError("Telegram configuration is required.")

    return result["bot"], result["chat"]