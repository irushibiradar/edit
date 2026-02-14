# भावपूर्णख — Telegram Menu Bot

A Telegram bot that serves the भावपूर्णख restaurant menu with live search, built in Python.

## Features

- `/start` — Interactive buttons to browse menu sections
- `/menu` — View the full menu
- **Live search** — Type any word (e.g. `वडापाव`, `डोसा`, `चहा`, `35`) to search
- All 40 items across 4 categories: नाश्ता, गोड पदार्थ, थाळी, पेय

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the API token you receive

### 2. Install & Run

```bash
cd bhavpurnakh-telegram-bot
pip install -r requirements.txt
TELEGRAM_BOT_TOKEN="your-token-here" python bot.py
```

### 3. Use the Bot

Open your bot in Telegram and send `/start`.

## Files

| File | Description |
|---|---|
| `bot.py` | Main bot script with menu data and handlers |
| `menu.html` | Original HTML menu page (for reference) |
| `requirements.txt` | Python dependencies |
