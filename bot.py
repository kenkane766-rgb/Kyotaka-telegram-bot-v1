import logging
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from commands.kick import kick
from commands.unban import unban
from commands.help_cmd import help_command
from commands.info import info
from commands.ttp import ttp
from commands.lirik import lirik
from commands.ass import ass
from commands.boobs import boobs
from commands.hboobs import hboobs
from commands.ipinfo import ipinfo
from commands.darkgen import darkgen
from commands.darkweather import darkweather
from commands.defdark import defdark
from commands.darkquote import darkquote
from commands.ping import ping
from commands.uptime import uptime
from commands.nsfw import nsfw
from commands.ai_kyo import ai_kyo
from commands.ban import ban
from commands.mute import mute
from commands.unmute import unmute
from commands.nightmode import nightmode
from commands.lock import lock
from commands.tagall import tagall
from commands.welcome import add_handler as add_welcome_handler
import time

import os

TOKEN = os.getenv("TELEGRAM_TOKEN", "7433451961:AAFqCDFtsVVhghwA3V77I0i3QA2-gyAerl8")
PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot Telegram DarkAI en ligne et actif 24/7"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes.")

async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot_data["start_time"] = time.time()

    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("kick", kick),
        CommandHandler("unban", unban),
        CommandHandler("ban", ban),
        CommandHandler("info", info),
        CommandHandler("ipinfo", ipinfo),
        CommandHandler("ttp", ttp),
        CommandHandler("lirik", lirik),
        CommandHandler("ass", ass),
        CommandHandler("boobs", boobs),
        CommandHandler("hboobs", hboobs),
        CommandHandler("darkgen", darkgen),
        CommandHandler("darkweather", darkweather),
        CommandHandler("defdark", defdark),
        CommandHandler("darkquote", darkquote),
        CommandHandler("ping", ping),
        CommandHandler("uptime", uptime),
        CommandHandler("nsfw", nsfw),
        CommandHandler("mute", mute),
        CommandHandler("unmute", unmute),
        CommandHandler("nightmode", nightmode),
        CommandHandler("lock", lock),
        CommandHandler("tagall", tagall),
        CommandHandler(["ai","kyo"], ai_kyo)
    ]

    for handler in handlers:
        application.add_handler(handler)
    
    add_welcome_handler(application)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Bot démarré et en écoute...")

    while True:
        await asyncio.sleep(3600)

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    bot_thread = threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True)

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()
