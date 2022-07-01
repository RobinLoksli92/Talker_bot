import os
from dotenv import load_dotenv
import logging

import telegram
from telegram import Update
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, CallbackContext, MessageHandler

from dialog_flow_detect_intents import detect_intents_text
from logs_handler import TelegramLogsHandler


logger = logging.getLogger('Logger')

states_db = {}


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = 'Приветствую'
    )
    return 'ECHO'


def reply_to_user(update: Update, context: CallbackContext):
    project_id = os.getenv('DF_PROJECT_ID')
    chat_id = update.message.chat_id
    response = detect_intents_text(project_id, session_id=chat_id, texts=[update.message.text])
    update.message.reply_text(
        text=response.query_result.fulfillment_text
    )
    return 'ECHO'


def handle_user_reply(update: Update, context: CallbackContext):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id

    else:
        return
    
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = 'ECHO'
    
    states_functions = {
        'START': start,
        'ECHO': reply_to_user
    }
    
    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_db.update({chat_id: next_state})
    

def main():
    load_dotenv()
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_bot = telegram.Bot(telegram_bot_token)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(telegram_bot))

    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_user_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply))
    updater.start_polling()


if __name__ == "__main__":
    main()