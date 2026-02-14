"""
भावपूर्णख - Telegram Menu Bot
A Telegram bot for browsing and searching the भावपूर्णख restaurant menu in Marathi.

Usage:
  1. Create a bot via @BotFather on Telegram and get your token
  2. Set the TELEGRAM_BOT_TOKEN environment variable
  3. Run: python bot.py
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Menu Data ──────────────────────────────────────────────────────────────────

SECTIONS = [
    {
        "title": "🍳 नाश्ता आणि स्नॅक्स",
        "key": "snacks",
        "items": [
            {"no": 1, "name": "उपीट", "price": 30},
            {"no": 2, "name": "शिरा", "price": 30},
            {"no": 3, "name": "इडली सांबर", "price": 35},
            {"no": 4, "name": "इडली वडा", "price": 45},
            {"no": 5, "name": "वडा सांबर", "price": 45},
            {"no": 6, "name": "आलूवडा", "price": 35},
            {"no": 7, "name": "मिरची भजे", "price": 30},
            {"no": 8, "name": "साधे भजे", "price": 35},
            {"no": 9, "name": "पूरी भाजी", "price": 35},
            {"no": 10, "name": "खिचडी", "price": 30},
            {"no": 11, "name": "मिसळ पाव", "price": 40},
            {"no": 12, "name": "पावभाजी", "price": 40},
            {"no": 13, "name": "वडापाव", "price": 15},
            {"no": 14, "name": "शाबु खिचडी", "price": 40},
            {"no": 15, "name": "शाबु वडा", "price": 50},
            {"no": 16, "name": "मसाला डोसा", "price": 40},
            {"no": 17, "name": "कट डोसा", "price": 50},
            {"no": 18, "name": "सादा डोसा", "price": 35},
            {"no": 19, "name": "उत्तप्पा", "price": 40},
            {"no": 20, "name": "दहीवडा", "price": 40},
        ],
    },
    {
        "title": "🍮 गोड पदार्थ",
        "key": "sweets",
        "items": [
            {"no": 21, "name": "जामुन", "price": 20},
            {"no": 22, "name": "बासुंदी", "price": 35},
            {"no": 23, "name": "डिंकलाई", "price": 20},
            {"no": 24, "name": "गंगा जामुन", "price": 50},
            {"no": 25, "name": "बालुशाई", "price": 20},
            {"no": 26, "name": "दहीभपाटी", "price": 40},
        ],
    },
    {
        "title": "🍛 थाळी, राईस",
        "key": "thali",
        "items": [
            {"no": 27, "name": "चपाती राईस प्लेट", "price": 90},
            {"no": 28, "name": "रोटी राईस प्लेट", "price": 100},
            {"no": 29, "name": "परोठा राईस प्लेट", "price": 90},
            {"no": 30, "name": "सिंगल राईस", "price": 60},
        ],
    },
    {
        "title": "☕ अतिरिक्त, पेय",
        "key": "extras",
        "items": [
            {"no": 31, "name": "एक्स्ट्रा रोटी", "price": 15},
            {"no": 32, "name": "एक्स्ट्रा चपाती", "price": 12},
            {"no": 33, "name": "भाजी वाटी", "price": 25},
            {"no": 34, "name": "वरण वाटी", "price": 25},
            {"no": 35, "name": "दही वाटी", "price": 20},
            {"no": 36, "name": "चहा", "price": 10},
            {"no": 37, "name": "स्पे. चहा", "price": 15},
            {"no": 38, "name": "स्पे. कॉफी", "price": 15},
            {"no": 39, "name": "डिकाशन", "price": 20},
            {"no": 40, "name": "स्पे. दूध", "price": 15},
        ],
    },
]


# ── Formatting Helpers ─────────────────────────────────────────────────────────


def format_item(item: dict) -> str:
    return f"  #{item['no']}  {item['name']}  —  ₹{item['price']}/-"


def format_section(section: dict) -> str:
    lines = [f"*{section['title']}*", ""]
    for item in section["items"]:
        lines.append(format_item(item))
    return "\n".join(lines)


def format_full_menu() -> str:
    header = "*भावपूर्णख — मेनू*\n"
    parts = [header]
    for sec in SECTIONS:
        parts.append(format_section(sec))
    return "\n\n".join(parts)


def search_menu(query: str) -> list[dict]:
    q = query.strip().lower()
    results = []
    for sec in SECTIONS:
        for item in sec["items"]:
            hay = f"{item['no']} {item['name']} {item['price']}".lower()
            if q in hay:
                results.append({**item, "section": sec["title"]})
    return results


# ── Bot Handlers ───────────────────────────────────────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📋 संपूर्ण मेनू", callback_data="menu_all")],
        [
            InlineKeyboardButton("🍳 नाश्ता", callback_data="menu_snacks"),
            InlineKeyboardButton("🍮 गोड", callback_data="menu_sweets"),
        ],
        [
            InlineKeyboardButton("🍛 थाळी", callback_data="menu_thali"),
            InlineKeyboardButton("☕ पेय", callback_data="menu_extras"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "*भावपूर्णख मध्ये आपले स्वागत आहे\\!*\n\n"
        "खालील बटणे वापरा किंवा मेनूमध्ये शोधण्यासाठी कोणताही शब्द टाइप करा\\.\n\n"
        "उदा: `वडापाव`, `डोसा`, `चहा`",
        parse_mode="MarkdownV2",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "*भावपूर्णख बॉट — मदत*\n\n"
        "/start — मुख्य मेनू बटणे\n"
        "/menu — संपूर्ण मेनू पहा\n"
        "/help — हे मदत संदेश\n\n"
        "कोणताही शब्द टाइप करा — मेनूमध्ये शोधा\n"
        "उदा: `वडापाव`, `डोसा`, `चहा`, `35`"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_full_menu(), parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu_all":
        text = format_full_menu()
    elif data.startswith("menu_"):
        key = data.replace("menu_", "")
        sec = next((s for s in SECTIONS if s["key"] == key), None)
        if sec:
            text = format_section(sec)
        else:
            text = "विभाग सापडला नाही."
    else:
        text = "अज्ञात क्रिया."

    await query.edit_message_text(text=text, parse_mode="Markdown")


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query_text = update.message.text.strip()
    if not query_text:
        return

    results = search_menu(query_text)

    if not results:
        await update.message.reply_text(
            f"'{query_text}' साठी काहीही सापडले नाही.\n"
            "वेगळा शब्द वापरून पहा किंवा /menu पहा."
        )
        return

    lines = [f"*🔍 शोध: '{query_text}'*", f"_{len(results)} पदार्थ सापडले_", ""]
    for r in results:
        lines.append(f"  #{r['no']}  {r['name']}  —  ₹{r['price']}/-")
        lines.append(f"     _{r['section']}_")
    text = "\n".join(lines)
    await update.message.reply_text(text, parse_mode="Markdown")


# ── Main ───────────────────────────────────────────────────────────────────────


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ERROR: Set the TELEGRAM_BOT_TOKEN environment variable.")
        print("  1. Talk to @BotFather on Telegram to create a bot")
        print("  2. Copy the token")
        print("  3. Run: TELEGRAM_BOT_TOKEN=<your-token> python bot.py")
        raise SystemExit(1)

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))

    logger.info("भावपूर्णख bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
