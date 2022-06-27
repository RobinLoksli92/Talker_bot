import os
from dotenv import load_dotenv
import json
import requests
from telegram import Update
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, CallbackContext, MessageHandler

from google.cloud import dialogflow


states_db = {}
project_id = 'sunlit-ace-354318'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = 'Приветствую'
    )
    return 'ECHO'


def echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = detect_intents_text(project_id, session_id=chat_id, texts=[update.message.text])
    update.message.reply_text(
        text=text
    )
    return 'ECHO'


def detect_intents_text(project_id, session_id, texts, language_code='RU-ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    return response.query_result.fulfillment_text


def handle_user_reply(update: Update, context: CallbackContext):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id

    else:
        return
    
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = states_db.get(chat_id)
    
    states_functions = {
        'START': start,
        'ECHO': echo
    }
    
    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_db.update({chat_id: next_state})
    

def main():
    load_dotenv()
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_user_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply ))
    updater.start_polling()


if __name__ == "__main__":
    main()