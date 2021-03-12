#!/usr/bin/env python3
from config import TOKEN
import subprocess
import logging
from telegram import Update
import telegram
from telegram.ext import Updater, CallbackContext, filters, MessageHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

REQUEST_KWARGS={
    'proxy_url': 'http://127.0.0.1:7890/',
}

def validate_youtube_link(update: Update, context: CallbackContext) -> None:
    msg = update.message.text
    _youtube_link = ["https://www.youtube.com/watch?v=", "https://youtu.be/"]
    for line in _youtube_link:
        if line in msg:
            youtube_dl(msg, update, context)
            return
    logger.warning(f"{msg} is a not a valide youtube link")

def youtube_dl(url: str, update: Update, context: CallbackContext) -> None:
    ydl = subprocess.Popen(["youtube-dl", "-v", url])
    ydl.wait()
    if (ydl.returncode == 0):
        logger.info(f"Download of {url} Succeeded")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Download of {url} Succeeded")
    else:
        logger.warning(f"Download of {url} Failed")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Download of {url} Failed")

updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)

updater.dispatcher.add_handler(MessageHandler(filters.Filters.text, validate_youtube_link))
updater.start_polling()
updater.idle()