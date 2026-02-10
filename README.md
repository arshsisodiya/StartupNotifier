# StartupNotifier 

StartupNotifier is a lightweight Windows background application that sends you a Telegram message every time your system starts.
It’s useful for monitoring system restarts, detecting unexpected reboots, or simply knowing when your PC is turned on — even when you’re away.

---

## Features

* Runs silently in the background
* Automatically starts with Windows boot
* Sends instant notifications via Telegram Bot API
* Minimal resource usage
* No UI required (headless background app)
* Easy configuration

---

## How It Works

1. The app is registered to run on Windows startup.
2. When the system boots, the app launches automatically.
3. It sends a predefined message to your Telegram chat using a Telegram bot.
4. The app exits or stays idle (based on configuration).

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
git clone https://github.com/arshsisodiya/StartupNotifier.git
cd StartupNotifier
```

### 2. Create a Telegram Bot

* Open Telegram and search for **@BotFather**
* Create a new bot and copy the **Bot Token**

### 3. Get Your Chat ID

* Start a chat with your bot
* Send any message
* Use Telegram Bot API or a helper script to fetch your `chat_id`

### 4. Configure the App

Edit the configuration in `config.py` (or `.env`, depending on your setup):

```
BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"
MESSAGE = "🖥️ Your system has started successfully!"
```

### 5. Run the App (Development)

```
python main.py
```

### 6. Build Windows Executable

```
pyinstaller --onefile --noconsole main.py
```

The executable will be available in the `dist/` folder.

### 7. Add to Windows Startup

**Startup Folder**

* Press `Win + R`
* Type `shell:startup`
* Paste the `.exe` or its shortcut

**Registry (Advanced)**

* Add an entry under:
  `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`

---

## Example Notification

```
🖥️ System Startup Alert
Your PC was powered on at 09:12 AM
```

---

## Use Cases

* Detect unauthorized system access
* Monitor remote PCs
* Track unexpected restarts
* Personal automation experiments

---

## Security Notes

* Keep your bot token private
* Do not commit secrets to GitHub
* Use environment variables for production builds

---

## Future Enhancements

* Shutdown notifications
* System info in messages (username, IP, uptime)
* Retry mechanism on network failure
* Log file support
* Tray icon mode

---

## License

MIT License

---

Made with ❤️ for automation and peace of mind.
