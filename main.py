import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Token del bot (lo cargás en Render como variable de entorno)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Endpoint de Vercel (tu URL pública)
VERCEL_ENDPOINT = "https://tu-app.vercel.app/api/audio"

def start(update, context):
    update.message.reply_text("Mandame un link de YouTube y te paso el audio 🎵")

def youtube_audio(update, context):
    url = update.message.text
    try:
        resp = requests.post(VERCEL_ENDPOINT, json={"url": url})
        if resp.status_code == 200:
            audio_url = resp.json().get("audio_url")
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_url)
        else:
            update.message.reply_text("Error al procesar el video 😔")
    except Exception as e:
        update.message.reply_text(f"Hubo un problema: {e}")

updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, youtube_audio))

updater.start_polling()