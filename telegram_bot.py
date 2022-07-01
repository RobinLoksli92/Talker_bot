import functools
import os
from dotenv import load_dotenv
import logging
import functools

import telegram
from telegram import Update
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, CallbackContext, MessageHandler

from dialog_flow_detect_intents import detect_intents_text
from logs_handler import TelegramLogsHandler


logger = logging.getLogger('Logger')


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = 'Приветствую'
    )
    return reply_to_user


def reply_to_user(update:Update, context:CallbackContext, project_id):
    chat_id = update.message.chat_id
    response = detect_intents_text(project_id, session_id=chat_id, texts=[update.message.text])
    update.message.reply_text(
        text=response.query_result.fulfillment_text
    )
    return reply_to_user


def main():
    load_dotenv()
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_bot = telegram.Bot(telegram_bot_token)
    logs_tg_id = os.getenv('USER_ID')

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(telegram_bot, logs_tg_id))

    project_id = os.getenv('DF_PROJECT_ID')
    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    reply = functools.partial(project_id=project_id)
    dispatcher.add_handler(MessageHandler(
        Filters.text,
        reply))
    updater.start_polling()


if __name__ == "__main__":
    main()