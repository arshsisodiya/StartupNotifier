# StartupNotifier 🚀

StartupNotifier is a lightweight Windows background application that sends you a Telegram message whenever your system starts.
It also supports remote commands via Telegram, allowing you to ping the system or capture screenshots on demand.

---

## Features

* Runs silently in the background
* Automatically starts with Windows boot
* Sends instant startup notifications via Telegram
* Supports Telegram commands:

  * `/ping` – check if the system is online
  * `/screenshot` – capture and send the current screen
* Configurable startup delay
* Minimal resource usage
* No UI required (headless background app)

---

## How It Works

1. The app is registered to run on Windows startup.
2. On boot, it waits for a configurable delay.
3. Sends a startup notification to your Telegram chat.
4. Listens for Telegram commands in the background.
5. Executes allowed commands securely and responds via Telegram.

---

## Tech Stack

* Python
* Telegram Bot API
* Windows Startup (Registry / Startup Folder)
* PyInstaller (for `.exe` build)

---

## Requirements

* Windows 10 / 11
* Python 3.9+ (for development)
* Telegram Bot Token
* Telegram Chat ID

---

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/StartupNotifier.git
cd StartupNotifier
```

---

### 2. Create a Telegram Bot

* Open Telegram and search for **@BotFather**
* Create a new bot
* Copy the **Bot Token**

---

### 3. Get Your Chat ID

* Start a chat with your bot
* Send any message
* Use Telegram Bot API or a helper script to fetch your `chat_id`

---

### 4. Configure the App (`config.json`)

StartupNotifier uses a **JSON-based configuration file**.

Create or edit `config.json` in the project root:

```json
{
  "ui_mode": "normal",
  "startup_delay": 15,

  "logging": {
    "level": "info"
  },

  "telegram": {
    "bot_token": "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE",
    "chat_id": "PASTE_YOUR_CHAT_ID_HERE"
  }
}
```

#### Configuration Options

* **ui_mode**

  * `normal` – background mode (recommended)
* **startup_delay**

  * Delay (in seconds) before sending startup notification
* **logging.level**

  * `info`, `debug`, `error`
* **telegram.bot_token**

  * Your Telegram bot token
* **telegram.chat_id**

  * Your personal or group chat ID

---

### 5. Run the App (Development)

```
python main.py
```

---

### 6. Build Windows Executable

```
pyinstaller --onefile --noconsole main.py
```

The executable will be generated inside the `dist/` folder.

---

### 7. Add to Windows Startup

#### Startup Folder (Recommended)

* Press `Win + R`
* Type `shell:startup`
* Paste the `.exe` or its shortcut

#### Registry (Advanced)

Add an entry under:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

---

## Telegram Commands

### `/ping`

Checks whether the system is online and responsive.

**Response example:**

```
✅ System is online
Uptime: 2h 14m
```

---

### `/screenshot`

Captures the current screen and sends it directly to your Telegram chat.

**Use cases:**

* Remote monitoring
* Checking system state
* Verifying active sessions

---

## Example Startup Notification

```
🖥️ System Startup Alert
Your PC has started successfully.
```

---

## Use Cases

* Detect unauthorized system access
* Monitor remote PCs
* Track unexpected restarts
* Remote system visibility via Telegram
* Personal automation experiments

---

## Security Notes

* Keep your bot token private
* Do not commit `config.json` with real credentials
* Add `config.json` to `.gitignore`
* Only predefined commands are supported

---

## Future Enhancements

* Shutdown notifications
* System info in startup message
* Multi-user access control
* Command permission levels
* Auto-update support

---

## License

MIT License

---

Made with ❤️ for automation, security, and peace of mind.

---
